
class Employee:
    # 初始化
    # id是Python的内建名字,就改成emp_id了,为了一致性,name也转换成了emp_name
    def __init__(self, emp_id:int, emp_name:str):
        self.emp_id = emp_id
        self.emp_name = emp_name
        self.reports = []

    def getId(self)->int:
        return self.emp_id

    def getReports(self)->[]:
        return self.reports

    def addReports(self, employee):
        self.reports.append(employee)

    # 遍历所有以本身为根节点的路径
    def _getAllPath(self, report_path: [])->{}:
        # 先把自己加入到路径中
        report_path.append(self)
        # 先把自己加入到合集中,这里要用拷贝,而不是引用
        self_report_path = report_path[:]
        # 为了兼容3.2
        # self_report_path = report_path.copy()
        self_dict = {self.emp_id: self_report_path}
        for one_emp in self.getReports():
            # 枚举每个reporter,看看有没有更底层的
            sub_dict = one_emp._getAllPath(self_report_path)
            # 等别人的都遍历完了,添加上自己的路径,一起合并到路径表里
            self_dict.update(sub_dict)
            # 遍历隔壁的孩子时先弹出刚遍历的孩子
            self_report_path.pop()
        return self_dict

    def __repr__(self):
        return self.emp_name

    @staticmethod
    def closetCommonManager(ceo, firstEmployee, secondEmployee):
        # 检查输入的参数
        if not(isinstance(ceo, Employee) and isinstance(firstEmployee, Employee) and isinstance(secondEmployee, Employee)):
            raise ValueError("ceo or first_employee or second_employee is not Employee")
        if firstEmployee.emp_id == secondEmployee.emp_id:
            raise ValueError("first and second employee are same.")

        all_path = ceo._getAllPath([])
        # 根据id得到路径
        try:
            first_path = all_path[firstEmployee.getId()]
            second_path = all_path[secondEmployee.getId()]
        except KeyError as e:
            error_id = int(str(e))
            if error_id == firstEmployee.emp_id:
                raise ValueError("firstEmployee not in ceo's manage scope")
            else:
                raise ValueError("secondEmployee not in ceo's manage scope")

        same_parent = None
        # 将两条路径组合
        for first_parent, second_parent in zip(first_path, second_path):
            if first_parent == second_parent:
                same_parent = first_parent
            else:
                break
        return same_parent

