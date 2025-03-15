## **一、项目架构**

### 用户服务智能体框架

```mermaid
graph LR
    A[User Interface] -->|HTTP/WebSocket| B[Services Layer]
    B -->|REST/GraphQL| C1[Core Layer]
    B -->|WebSocket| C2[Realtime Pipeline]
    
    subgraph Services Layer
        B1[HTTP/REST API]
        B2[GraphQL API]
        B3[WebSocket Server]
        B4[Map Service]
    end

    subgraph Core Layer
        C1 --> D1[NLP Processor]
        C1 --> D2[Dork Generator]
        C1 --> D3[Darkweb Crawler]
        C1 --> D4[ARP Scanner]
    end

    subgraph Data Engine
        C2 --> E1[Hybrid Index]
        C2 --> E2[Realtime Pipeline]
        E1 --> F1[B-Tree Index]
        E1 --> F2[Elasticsearch Adapter]
        E2 --> F3[Kafka Ingestion]
        E2 --> F4[Stream Processor]
    end

    subgraph Adapters Layer
        G1[Database Connector]
        G2[Darkweb Adapter]
        G3[IoT Protocols]
        G1 --> H1[SQLite]
        G2 --> H3[Tor Client]
        G3 --> H4[MQTT]
        G3 --> H5[CoAP]
    end

    subgraph Infrastructure
        I1[Caching]
        I2[Monitoring]
        I3[Security]
        I1 --> J1[Redis Cluster]
        I2 --> J2[Performance Metrics]
        I2 --> J3[Security Audit]
        I3 --> J4[Tor Management]
        I3 --> J5[Crypto Engine]
    end

    subgraph Utils
        K1[Behavioral Analysis]
        K2[Query Optimizer]
        K1 --> L1[User Profiling]
        K2 --> L2[Ranking Algorithm]
        K2 --> L3[Cost Calculator]
    end

    subgraph File Parsers
        M1[Legacy Parser]
        M2[Unified Parser]
        M1 --> N1[CSV]
        M1 --> N2[PDF]
        M2 --> N3[JSON]
        M2 --> N4[XML]
    end

    A -->|User Input| B
    B -->|Processed Data| A
    C1 -->|Query| G1
    G1 --> |storage|C1
    C1 -->|Fetch| G2
    C1 -->|Scan| G3
    E1 -->|Index Data| G1
    E2 -->|Stream Data| G1
    I1 -->|Cache Data| B
    I2 -->|Monitor| B
    I3 -->|Secure| B
    K1 -->|Analyze| B
    K2 -->|Optimize| C1
    M1 -->|Parse| G1
    M2 -->|Parse| G1
```

 

### 实时更新脚本工作流

```mermaid
graph TD
    A[每五分钟获取一次数据源] -->|通过程序轮询或推送| B[消息队列Kafka]
    B --> |复用| C[数据清洗（和答案集合-这个不用）智能体]
    C --> D[更新SQLite]
    C --> E[更新Elasticsearch]
    D --> G
    E --> G[数据库]
```



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
## 3. moxin(coming...)

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

## 8. Python modules




# 三、展示

## 搜索页

![1](asset/1.png)

## 结果页

![1](asset/2.png)

![2](asset/3.png)