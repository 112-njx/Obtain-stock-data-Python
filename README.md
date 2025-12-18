# Obtain-stock-data-Python
基于Python QMT 接口，获取并分析各大平台的A股股票数据及简单的技术分析，是量化投资入门的不二之选，配有详细注释。
项目结构：
project/
│
├── main.py                # 程序入口，负责整体流程调度
├── data_fetcher.py        # 行情数据获取模块
├── data_processor.py     # 数据清洗与整理模块
├── indicators.py          # 技术指标计算模块
├── strategy.py            # 投资建议生成模块
└── config.py              # 参数配置（如指标周期）
