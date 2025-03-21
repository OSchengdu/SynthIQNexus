from fastapi import FastAPI, Query, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
import markdown
import datetime
import asyncio

app = FastAPI()

# 启用 CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟数据存储
sample_data = [
    {
        "trigger": "dork",
        "title": "Dork 搜索结果总结",
        "description": """
## 相关链接
- [示例链接1](https://example.com/dork1)
- [示例链接2](https://example.com/dork2)

## 统计信息
- 总结果数：2
- 相关度：0.85
        """,
        "relevance": 0.85,
        "timestamp": "刚刚"
    },
    {
        "trigger": "dork",
        "title": "Dork 搜索结果总结",
        "description": """
## 相关链接
- [示例链接1](https://example.com/dork1)
- [示例链接2](https://example.com/dork2)

## 统计信息
- 总结果数：2
- 相关度：0.85
        """,
        "relevance": 0.85,
        "timestamp": "刚刚"
    },

    {
        "trigger": "dork",
        "title": "Dork 搜索结果总结",
        "description": """
## 相关链接
- [示例链接1](https://example.com/dork1)
- [示例链接2](https://example.com/dork2)

## 统计信息
- 总结果数：2
- 相关度：0.85
        """,
        "relevance": 0.85,
        "timestamp": "刚刚"
    },
    {
        "trigger": "dork",
        "title": "Dork 搜索结果总结",
        "description": """
## 相关链接
- [示例链接1](https://example.com/dork1)
- [示例链接2](https://example.com/dork2)

## 统计信息
- 总结果数：2
- 相关度：0.85
        """,
        "relevance": 0.85,
        "timestamp": "刚刚"
    },
]

# 定义请求和响应模型
class AgentOutput(BaseModel):
    content: str  # 智能体的输出内容

class SearchResult(BaseModel):
    trigger: str
    title: str
    description: str
    relevance: float
    timestamp: str

class SearchResponse(BaseModel):
    results: List[SearchResult]

# 接收智能体输出的接口
@app.post("/agent-output")
async def receive_agent_output(output: AgentOutput):
    try:
        # 这里可以处理智能体的输出，例如存储到数据库或添加到 sample_data
        print("Received agent output:", output.content)
        return {"status": "success", "message": "Agent output received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process agent output: {str(e)}")

# 搜索接口
@app.get("/search", response_model=SearchResponse)
async def search(
    query: Optional[str] = Query(None, description="搜索关键词"),
    trigger: Optional[str] = Query(None, description="结果来源标签")
):
    # 过滤逻辑
    filtered_results = sample_data
    if query:
        filtered_results = [result for result in filtered_results if query.lower() in result["description"].lower()]
    if trigger:
        filtered_results = [result for result in filtered_results if result["trigger"] == trigger]

    # 返回结果
    return {"results": filtered_results}

# Markdown 渲染接口（可选）
@app.post("/render-markdown")
async def render_markdown(content: str = Body(..., embed=True)):
    try:
        html_content = markdown.markdown(content)
        return {"html": html_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Markdown 渲染失败: {str(e)}")

# 健康检查接口
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}
