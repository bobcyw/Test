class Employee:
    # 初始化
    # id是Python的内建名字,就改成emp_id了,为了一致性,name也转换成了emp_name
    def __init__(self, emp_id: int, emp_name: str):
        self._emp_id = emp_id
        self._emp_name = emp_name
        self._reports = []

    @property
    def emp_name(self)->str:
        return self._emp_name

    # 这里注释掉,默认emp_name之类的设计都是const,原则上不解开这里的代码
    # @emp_name.setter
    # def emp_name(self, val):
    #     self._emp_name = val

    @property
    def emp_id(self)->int:
        return self._emp_id

    # 同理emp_name
    # @emp_id.setter
    # def emp_id(self, val)->int:
    #     self._emp_id = val

    @property
    def reports(self)->[]:
        return self._reports

    def add_reports(self, employee):
        self.reports.append(employee)

    def get_all_path(self):
        """
        对外的接口,屏蔽掉一些细节
        :return: 返回一个字典,{emp_id: [一个从ceo开始到本身的路径]}
        """
        return self.get_all_path_with_path([])

    def get_all_path_with_path(self, report_path: [])->{}:
        """
        遍历所有以本身为根节点的路径,真实算法所在
        :param report_path: 初始的给[]这样的空值
        :return: 同get_all_path
        """
        # 先把自己加入到路径中
        report_path.append(self)
        # 先把自己加入到合集中,这里要用拷贝,而不是引用
        self_report_path = report_path[:]
        self_dict = {self.emp_id: self_report_path}
        for one_emp in self.reports:
            # 枚举每个reporter,看看有没有更底层的
            sub_dict = one_emp.get_all_path_with_path(self_report_path)
            # 等别人的都遍历完了,添加上自己的路径,一起合并到路径表里
            self_dict.update(sub_dict)
            # 遍历隔壁的孩子时先弹出刚遍历的孩子
            self_report_path.pop()
        return self_dict

    def __repr__(self):
        return self.emp_name


def closet_common_manager(ceo: Employee, first_employee: Employee, second_employee: Employee)->Employee:
    """ 得到our boss
    :param ceo: 起始节点,Employee
    :param first_employee: 第一个雇员, Employee
    :param second_employee: 第二个雇员, Employee
    :return: 一般会返回一个正确的结果,
    异常情况:Employee.EmployeeNotIn -> 雇员不在ceo管辖范围
            Employee.SameEmployee -> 给出的雇员相同
            Employee.ErrorEmployee -> 雇员参数给错了
    """
    # 检查输入的参数
    if not isinstance(ceo, Employee) or not isinstance(first_employee, Employee) or not isinstance(second_employee,
                                                                                                   Employee):
        raise ValueError("ceo or first_employee or second_employee is not Employee")
    if first_employee.emp_id == second_employee.emp_id:
        raise ValueError("first and second employee are same.")
    # 根据id得到路径
    all_path = ceo.get_all_path()
    try:
        first_path = all_path[first_employee.emp_id]
        second_path = all_path[second_employee.emp_id]
    except KeyError as e:
        error_id = int(str(e))
        if error_id == first_employee.emp_id:
            raise ValueError("first_employee not in ceo's manage scope")
        else:
            raise ValueError("second_employee not in ceo's manage scope")
    same_parent = None
    # 将两条路径组合
    for first_parent, second_parent in zip(first_path, second_path):
        if first_parent == second_parent:
            same_parent = first_parent
        else:
            break
    return same_parent


def closet_common_manager2(all_path: {}, first_employee: Employee, second_employee: Employee)->Employee:
    """ 得到our boss
    :param all_path: 由Employ.get_all_path得到的全雇员路径图
    :param first_employee: 第一个雇员, Employee
    :param second_employee: 第二个雇员, Employee
    :return: 一般会返回一个正确的结果,但是也有可能抛出一个雇员不在ceo范围的异常EmployeeNotIn,特别当第一个和第二个雇员中有一个不在ceo的管辖范围时
    """
    # 检查输入的参数
    if isinstance(all_path, dict) is False:
        raise ValueError("all_path should be a dict")
    if not(isinstance(first_employee, Employee) and isinstance(second_employee, Employee)):
        raise ValueError("first_employee or second_employee is not Employee")
    if first_employee.emp_id == second_employee.emp_id:
        raise ValueError("first and second employee are same.")

    # 根据id得到路径
    try:
        first_path = all_path[first_employee.emp_id]
        second_path = all_path[second_employee.emp_id]
    except KeyError as e:
        error_id = int(str(e))
        if error_id == first_employee.emp_id:
            raise ValueError("first_employee not in ceo's manage scope")
        else:
            raise ValueError("second_employee not in ceo's manage scope")
    same_parent = None
    # 将两条路径组合
    for first_parent, second_parent in zip(first_path, second_path):
        if first_parent == second_parent:
            same_parent = first_parent
        else:
            break
    return same_parent
