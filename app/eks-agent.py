#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from datetime import datetime
from mcp import stdio_client, StdioServerParameters
from strands.models import BedrockModel, OpenRouterModel
from strands import Agent
from strands.tools.mcp import MCPClient

def quiet_stdio_client(params: StdioServerParameters):
    """Wrap stdio_client to silence subprocess output."""
    return stdio_client(
        StdioServerParameters(
            command=params.command,
            args=params.args,
            env=params.env,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    )

def main():
    parser = argparse.ArgumentParser(description='AWS EKS MCP Agent - Problem Detection with Fixes')
    parser.add_argument('--provider', '-p', default='bedrock', choices=['bedrock', 'openrouter'])
    parser.add_argument('--cluster', '-c', required=True)
    
    args = parser.parse_args()
    
    print(f"🔍 Inspecting cluster: {args.cluster}")
    print(f"🤖 Provider: {args.provider}")
    print("-" * 60)

    mcp_env = os.environ.copy()
    mcp_env['FASTMCP_LOG_LEVEL'] = 'ERROR'

    mcp_client = MCPClient(lambda: quiet_stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["awslabs.eks-mcp-server@latest", "--allow-sensitive-data-access"],
            env=mcp_env
        )
    ))
    
    try:
        with mcp_client:
            all_tools = mcp_client.list_tools_sync()
            
            desired_tool_names = [
                'get_eks_vpc_config',
                'list_k8s_resources', 
                'get_k8s_events',
                'get_pod_logs',
                'search_eks_troubleshoot_guide'
            ]

            tools = [tool for tool in all_tools if hasattr(tool, 'tool_name') and tool.tool_name in desired_tool_names]
            
            print(f"✅ Using {len(tools)} tools:")
            for tool in tools:
                print(f"   - {tool.tool_name}")

            if args.provider == 'bedrock':
                model = BedrockModel(
                    model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
                    region_name="us-east-1",
                    temperature=0.2,
                )
            else:
                model = OpenRouterModel(
                    model_id="anthropic/claude-sonnet-4",
                    temperature=0.2,
                )
            
            agent = Agent(tools=tools, model=model)
            
            query = f"""
            ROLE: 
            You are a senior SRE responding to a production outage.
            MISSION:
            Check EKS cluster '{args.cluster}' ONLY for problems and provide specific commands for fixing.
            CRITICAL RULES:
               - Use only fresh, real-time data.Do not rely on cached results.
               - Skip insights and healthy components.
               - Output only findings and remediation commands. Skip other comments about architecture and setup or any other fluff.
            4.OUTPUT FORMAT:
            CURRENT TIME: [UTC current timestamp]
            PROBLEM: [brief description]
            FIX: [specific fix command copy-paste ready]
            VERIFY: [specific verification command copy-paste ready]
            """

            response = agent(query) 

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
