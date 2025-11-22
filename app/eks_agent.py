#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from datetime import datetime
from mcp import stdio_client, StdioServerParameters
from strands.models import BedrockModel
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
            stderr=subprocess.DEVNULL,  # discard all stderr output
        )
    )

def main():
    parser = argparse.ArgumentParser(description='AWS EKS MCP Agent - Problem Detection with Fixes')
    parser.add_argument('--account-id', '-a', required=True)
    parser.add_argument('--region', '-r', required=True)
    parser.add_argument('--cluster-name', '-c', required=True)
    
    args = parser.parse_args()
    
    print(f"🔍 Inspecting cluster: {args.cluster_name}")
    print(f"🏢 AWS Account: {args.account_id}")
    print(f"🌍 AWS Region: {args.region}")
    print("-" * 60)

    # Create modified environment with reduced log level for MCP server
    mcp_env = os.environ.copy()
    mcp_env['FASTMCP_LOG_LEVEL'] = 'ERROR'  # Suppress INFO and WARNING messages

    # Use the quiet version to silence INFO messages
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

            # Create Bedrock model instance 
            bedrock_model = BedrockModel(
                model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
                region_name="us-east-1",
                temperature=0.2,
            )
            agent = Agent(tools=tools, model=bedrock_model)
            
            query = f"""
            ROLE: 
            You are a senior SRE responding to a production outage.
            MISSION:
            Check EKS cluster '{args.cluster_name}' ONLY for problems and provide specific commands for fixing.
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
            
            #print("\nRESULTS:")
            #print("=" * 40)
            #print(response)
            
            # Return response for potential programmatic use
            #return response

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
