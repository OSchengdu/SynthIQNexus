from typing import List, Dict, Any
import pandas as pd
import plotly.express as px

class DiagramGenerator:
    def __init__(self, results: List[Dict[str, Any]]):
        """
        初始化 DiagramGenerator。
        
        :param results: 查询结果，格式为字典列表。
        """
        self.results = results
        self.df = pd.DataFrame(results)  # 将结果转换为 DataFrame 以便分析

    def _detect_chart_type(self) -> str:
        """
        根据数据特征选择合适的图表类型。
        
        :return: 图表类型（如 "bar", "line", "pie", "scatter" 等）。
        """
        # 规则 1：如果有时间字段，生成折线图
        if "Time Period" in self.df.columns and "Data Value" in self.df.columns:
            return "line"

        # 规则 2：如果有分类字段，生成饼图
        if "Name" in self.df.columns and "Data Value" in self.df.columns:
            return "pie"

        # 规则 3：如果有两个数值字段，生成散点图
        if "Data Value" in self.df.columns and "Indicator ID" in self.df.columns:
            return "scatter"

        # 默认生成柱状图
        return "bar"

    def generate_chart_data(self) -> Dict[str, Any]:
        """
        生成图表数据。
        
        :return: 包含图表类型和数据的字典。
        """
        chart_type = self._detect_chart_type()
        chart_data = {}

        if chart_type == "line":
            # 生成折线图数据
            chart_data["type"] = "line"
            chart_data["data"] = {
                "x": self.df["Time Period"].tolist(),
                "y": self.df["Data Value"].tolist(),
            }
        elif chart_type == "pie":
            # 生成饼图数据
            chart_data["type"] = "pie"
            chart_data["data"] = {
                "labels": self.df["Name"].tolist(),
                "values": self.df["Data Value"].tolist(),
            }
        elif chart_type == "scatter":
            # 生成散点图数据
            chart_data["type"] = "scatter"
            chart_data["data"] = {
                "x": self.df["Indicator ID"].tolist(),
                "y": self.df["Data Value"].tolist(),
            }
        else:
            # 默认生成柱状图数据
            chart_data["type"] = "bar"
            chart_data["data"] = {
                "x": self.df["Name"].tolist(),
                "y": self.df["Data Value"].tolist(),
            }

        return chart_data

    def generate_plotly_figure(self):
        """
        使用 Plotly 生成交互式图表。
        
        :return: Plotly 图表对象。
        """
        chart_type = self._detect_chart_type()

        if chart_type == "line":
            fig = px.line(
                self.df,
                x="Time Period",
                y="Data Value",
                title="Data Value Over Time",
            )
        elif chart_type == "pie":
            fig = px.pie(
                self.df,
                names="Name",
                values="Data Value",
                title="Data Value Distribution",
            )
        elif chart_type == "scatter":
            fig = px.scatter(
                self.df,
                x="Indicator ID",
                y="Data Value",
                title="Data Value vs Indicator ID",
            )
        else:
            fig = px.bar(
                self.df,
                x="Name",
                y="Data Value",
                title="Data Value by Name",
            )

        return fig

    def generate_html_embed(self) -> str:
        """
        生成嵌入网页的 HTML 代码。
        
        :return: 包含 Plotly 图表的 HTML 代码。
        """
        fig = self.generate_plotly_figure()
        return fig.to_html(full_html=False)


# 示例用法
if __name__ == "__main__":
    # 示例数据
    example_results = [
        {
            "Unique ID": 221956,
            "Indicator ID": 386,
            "Name": "Ozone (O3)",
            "Measure": "Mean",
            "Measure Info": "ppb",
            "Geo Type Name": "UHF34",
            "Geo Join ID": 305307,
            "Geo Place Name": "Upper East Side-Gramercy",
            "Time Period": "Summer 2014",
            "Start_Date": "06/01/2014",
            "Data Value": 24.9,
            "Message": "http://example.com/data/221956",
        },
        {
            "Unique ID": 221806,
            "Indicator ID": 386,
            "Name": "Ozone (O3)",
            "Measure": "Mean",
            "Measure Info": "ppb",
            "Geo Type Name": "UHF34",
            "Geo Join ID": 103,
            "Geo Place Name": "Fordham - Bronx Pk",
            "Time Period": "Summer 2014",
            "Start_Date": "06/01/2014",
            "Data Value": 30.7,
            "Message": "http://example.com/data/221806",
        },
    ]

    # 初始化 DiagramGenerator
    diagram_generator = DiagramGenerator(example_results)

    # 生成图表数据
    chart_data = diagram_generator.generate_chart_data()
    print("图表数据：", chart_data)

    # 生成嵌入网页的 HTML 代码
    html_embed = diagram_generator.generate_html_embed()
    print("HTML 嵌入代码：", html_embed)

    # 生成 Plotly 图表
    fig = diagram_generator.generate_plotly_figure()
    fig.show()  # 显示图表
