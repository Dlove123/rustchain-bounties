#!/usr/bin/env python3
"""
BoTTube MCP Server - Model Context Protocol integration for BoTTube
Allows Claude Code to interact with BoTTube platform
"""

from mcp.server.fastmcp import FastMCP
import requests

# Initialize MCP server
mcp = FastMCP("BoTTube")

# Configuration
BOTTUBE_API_URL = "https://api.bottube.com"


@mcp.tool()
def get_video_info(video_id: str) -> dict:
    """
    Get BoTTube video information.
    
    Args:
        video_id: BoTTube video ID
        
    Returns:
        Video information including title, views, votes
    """
    try:
        response = requests.get(f"{BOTTUBE_API_URL}/videos/{video_id}", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def search_videos(query: str, limit: int = 10) -> list:
    """
    Search BoTTube videos.
    
    Args:
        query: Search query
        limit: Maximum results (default: 10)
        
    Returns:
        List of matching videos
    """
    try:
        response = requests.get(
            f"{BOTTUBE_API_URL}/search",
            params={"q": query, "limit": limit},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
def get_user_profile(username: str) -> dict:
    """
    Get BoTTube user profile.
    
    Args:
        username: BoTTube username
        
    Returns:
        User profile information
    """
    try:
        response = requests.get(f"{BOTTUBE_API_URL}/users/{username}", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def vote_video(video_id: str, vote_type: str) -> dict:
    """
    Vote on a BoTTube video.
    
    Args:
        video_id: Video ID
        vote_type: 'upvote' or 'downvote'
        
    Returns:
        Vote result
    """
    if vote_type not in ['upvote', 'downvote']:
        return {"error": "vote_type must be 'upvote' or 'downvote'"}
    
    try:
        response = requests.post(
            f"{BOTTUBE_API_URL}/videos/{video_id}/vote",
            json={"type": vote_type},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def upload_video(title: str, description: str, video_url: str) -> dict:
    """
    Upload a video to BoTTube.
    
    Args:
        title: Video title
        description: Video description
        video_url: URL to video file
        
    Returns:
        Upload result with video ID
    """
    try:
        response = requests.post(
            f"{BOTTUBE_API_URL}/videos/upload",
            json={
                "title": title,
                "description": description,
                "video_url": video_url
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_trending_videos(limit: int = 10) -> list:
    """
    Get trending BoTTube videos.
    
    Args:
        limit: Maximum results (default: 10)
        
    Returns:
        List of trending videos
    """
    try:
        response = requests.get(
            f"{BOTTUBE_API_URL}/trending",
            params={"limit": limit},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("videos", [])
    except Exception as e:
        return [{"error": str(e)}]


if __name__ == "__main__":
    mcp.run()
