## **一、项目架构**

### 用户服务智能体框架

```mermaid
graph LR
    A[用户输入] --> |自然语言| B(NLP解析智能体)
    H --> |用户满意| 完成,等待下一次输入 --> A
    B --> C{source_router脚本}
    
    C --> |有分析需求| Y[地图接入与处理智能体]
    Y --> |传递关键坐标、天气、地形、风速、风压、气压、热力分布等| F[数据清洗和答案集合智能体]
    
    C --> |Dork数据库| D[Dork智能体]
    D --> |传递搜索到的前30个相关结果| F
    
    C --> |数据库查询| Z[sqlLite数据库查询智能体]
    Z --> |传递语句查询到的数据结果| F
    
    C --> |终端操作| E[arp扫描智能体]
    E --> |传递终端扫描结果与报错| F
    
    C --> |传递三元组| F
    
    F --> |判断是否需要| M[diagram生成]
    M --> |不需要| Q[不生成]
    M --> |需要| H[用户界面输出框]
    
    F --> |传递清洗结果+choose_data脚本的输出| G[结果生成智能体]
    G --> H
    

    H --> |用户不满意| J[用户点击重新生成按钮]
    J --> B
```

 

### 实时更新脚本工作流

```mermaid
graph LR
    A[每五分钟获取一次数据源] -->|通过程序轮询或推送| B[消息队列Kafka]
    B --> |复用| C[数据清洗（和答案集合-这个不用）智能体]
    C --> D[更新SQLite]
    C --> E[更新Elasticsearch]
    D --> G
    E --> G[数据库]
```

# 

### 网页展示接口







# 二、环境配置

## 1. Elastisearch
## 2. mofa

```bash
git clone https://github.com/moxin-org/mofa.git
conda cerate -n py310 python=3.10.12 -y
cd mofa/python
pip install -r requirements.txt (if this command report error, never mind it
pip install -e .
python -V
python -c "import mofa" && echo "mofa install successfully"
```
## 3. moly

## 4. python env

## 5. cargo

## 6. dora
### 	Fedora

```bash
sudo dnf install cargo rustup dora-cli
cargo install dora-rs
pip install dora-cli

```

### 	Arch

```bash
sudo pacman -S  cargo rustup dora-cli
cargo install dora-rs
pip install dora-cli
```

## 7. FastAPI

# 三、展示

## 搜索页

![图片1](../Screenshot From 2025-03-07 12-04-08.png)

## 结果页

![图片2](../Screenshot From 2025-03-07 12-48-05.png)
![图片3](../Screenshot From 2025-03-07 12-48-01.png)
