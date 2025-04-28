class PageSalesPlan(BasePage):
    def __init__(self, driver):
        super().__init__(driver)  # 调用父类的初始化方法，传入driver对象

    # 定位器
    salesplan_button = ("xpath", "//span[text()='销售计划']")  # 销售计划按钮
    # 选择店铺
    # 选择市场
    # 查询ASIN
    # 创建需求
    search_button = ("xpath", "//button[text()='查询']")  # 查询按钮
    