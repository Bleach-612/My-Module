from pyecharts.charts import Bar, Line, Scatter
from pyecharts import options
# 内置主题类型
from pyecharts.globals import ThemeType
from pyecharts.globals import RenderType


class MyEcharts:
    def __init__(self, image_type='Bar', **kwargs):
        """
        初始化
        :param image_type: 图像类型, 默认柱状图(Bar)、折线图(Line)、散点图(Scatter),当前仅支持以上三种
        """
        self.image_type = image_type.title()  # 首字母大写
        self.module_name = 'pyecharts.charts.basic_charts.' + image_type.lower()
        self.obj = self.get_instance(self.module_name, self.image_type, **kwargs)

    @staticmethod
    def get_instance(module_name, class_name, *args, **kwargs):
        """
        获取实例化对象
        :param module_name: 模块名
        :param class_name: 类名
        :param args:
        :param kwargs:
        :return obj:
        """
        module_meta = __import__(module_name, globals(), locals(), [class_name])
        class_meta = getattr(module_meta, class_name)
        obj = class_meta(*args, **kwargs)
        return obj

    def add_yaxis(self, name, data):
        """设置y轴"""
        self.obj.add_yaxis(name, data)

    def add_xaxis(self, data):
        """设置x轴"""
        self.obj.add_xaxis(data)

    def set_series_opts(self, **kwargs):
        """系列配置,可控制图表中的文本、线样式、标记,具体参数可查看源码"""
        self.obj.set_series_opts(**kwargs)

    def set_global_opts(self, **kwargs):
        """全局配置，可控制图标中的标题、工具箱等，各参数对象还可设置其他参数,具体参数可查看源码
            title_opts——标题
            legend_opts——图例
            tooltip_opts——​提示框
            toolbox_opts——工具箱
            brush_opts——区域选择组件
            xaxis_opts——​X轴
            yaxis_opts——Y轴
            visualmap_opts——视觉映射
            datazoom_opts——​区域缩放
            graphic_opts——原生图形元素组件
            axispointer_opts——坐标轴指示器
        """
        self.obj.set_global_opts(**kwargs)

    def render(self, file_name='render.html'):
        """生成html文件"""
        self.obj.render(file_name)

    def make(self, x_data, y_name, y_data, file_name='render.html', **kwargs):
        """
        一键生成
        :param x_data: x轴数据
        :param y_data: y轴数据
        :param y_name: y轴名称
        :param file_name: 文件名
        :param **kwargs
        """
        self.obj.add_xaxis(x_data)
        self.obj.add_yaxis(y_name, y_data)
        self.obj.set_global_opts(**kwargs)
        self.obj.render(file_name)


def test():
    head = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    # 传递需要配置参数, 设置主题
    init_opts = options.InitOpts(
        width="900px",
        height='500px',
        page_title='wf_pyecharts',
        renderer=RenderType.SVG,    # renderer为渲染风格，只有"canvas","svg"两个选项,svg清晰度高一些。
        theme=ThemeType.LIGHT       # theme是图表主题
    )

    """手动创建柱状图"""
    my_echarts = MyEcharts('bar', init_opts=init_opts)
    my_echarts.add_xaxis(head)
    my_echarts.add_yaxis("商家A", [51, 201, 36, 101, 75, 90])
    my_echarts.add_yaxis("商家B", [151, 201, 136, 101, 175, 190])
    my_echarts.set_global_opts(
        legend_opts=options.LegendOpts(is_show=True),                    # 图例配置
        title_opts=options.TitleOpts(title='主标题', subtitle='副标题'),   # 主副标题
        toolbox_opts=options.ToolboxOpts(is_show=True, pos_left='80%'),  # 工具箱
    )
    my_echarts.render('outer.html')

    """一键生成折线图"""
    my_echarts = MyEcharts('line', init_opts=init_opts)
    my_echarts.make(
        x_data=head,
        y_name='商家A',
        y_data=[51, 201, 36, 101, 75, 90],
        legend_opts=options.LegendOpts(is_show=True),
        title_opts=options.TitleOpts(title='主标题', subtitle='副标题'),
        toolbox_opts=options.ToolboxOpts(is_show=True, pos_left='80%')
    )


if __name__ == '__main__':
    """
    Install cmd:    pip install pyecharts
    Demo URL:   https://zhuanlan.zhihu.com/p/127760528
    """
    test()
