from background import models
import datetime

def check_cookies(request):
    is_stu = True
    v = request.COOKIES.get('log_s')
    if not v:
        v = request.COOKIES.get('log_t')
        if not v:
            return False
        else:
            is_stu = False
    return True

def parse_UUID(uuid):
    """ 解析UUID 去掉-
    :param uuid: 需要解析的UUID
    :return: str
=======
 解析UUID 去掉-\n
    :param uuid: 需要解析的UUID\n
    :return: str\n
    """
    uuid = str(uuid)
    uuid_str = ''.join(uuid.split('-'))
    return uuid_str

# 创建课程签到信息函数
def set_sign(cid, time_start, time_end, debug=False):
    """ 创建课程签到信息函数
    :param cid: 课程编号
    :param time_start: 开始时间
    :param time_end: 结束时间
=======
    创建课程签到信息函数\n
    :param cid: 课程编号\n
    :param time_start: 开始时间\n
    :param time_end: 结束时间\n
    :return: 创建失败返回NoneType 创建成功返回课程签到信息主键
    """
    course = models.Course.objects.get(cid=cid)
    cousign_info = models.CouSignInfo.objects.filter(cid__cid=cid, timeend__gt=time_start)
    # 测试用
    if debug:
        return models.CouSignInfo.objects.create(cid=course, timestart=time_start, timeend=time_end)

    # 如果开始时间大于结束时间 或 还有正在进行中的签到 不予继续创建签到
    if time_start > time_end or cousign_info.exists():
        return None

    cousign = models.CouSignInfo.objects.create(cid=course, timestart=time_start, timeend=time_end)
    return cousign

# 学生签到函数
def student_sign(stuid, couid, cousignid, debug=False):
    """ 学生签到函数
    :param stuid: 学生学号
    :param couid: 课程编号
    :param cousignid: 签到UUID
=======
    学生签到函数\n
    :param stuid: 学生学号\n
    :param couid: 课程编号\n
    :param cousignid: 签到UUID\n
    :return: 返回学生签到状态字典
    """
    signInfo = {
        'isOutTime' : True,     # 是否在签到时间段
        'isInClass' : False,    # 是否为本课程学生
        'isSigned' : False      # 是否已经签到
    }

    try:
        stu = models.StuToCourse.objects.get(sid__sid=stuid, cid__cid=couid)
        signInfo['isInClass'] = True

        # 测试用
        if debug:
            models.SignInfo.objects.create(sid=stu.sid, cid=stu.cid)
            return signInfo

        if models.SignInfo.objects.filter(cid=cousignid).exists():
            signInfo['isSigned'] = True
            return signInfo

        # 获取课程详细信息
        time = datetime.datetime.now()
        if time >= cousignid.timestart and time <= cousignid.timeend :
            # 写入签到信息
            models.SignInfo.objects.create(sid=stu.sid, cid=stu.cid)
            signInfo['isOutTime'] = False
    except Exception:
        pass

    return signInfo


# 分页器代码：
class Pagination(object):
    def __init__(self, current_page, all_count, per_page_num=10, pager_count=7):
        """
        封装分页相关数据
        :param current_page: 当前页
        :param all_count:    数据库中的数据总条数
        :param per_page_num: 每页显示的数据条数
        :param pager_count:  最多显示的页码个数

        用法:
        queryset = model.objects.all()
        page_obj = Pagination(current_page,all_count)
        page_data = queryset[page_obj.start:page_obj.end]
        获取数据用page_data而不再使用原始的queryset
        获取前端分页样式用page_obj.page_html
        """
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page < 1:
            current_page = 1

        self.current_page = current_page

        self.all_count = all_count
        self.per_page_num = per_page_num

        # 总页码
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page * self.per_page_num

    def page_html(self):
        # 如果总页码 < 11个：
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码  > 11
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1

            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page + self.pager_count_half) > self.all_pager:
                    pager_end = self.all_pager + 1
                    pager_start = self.all_pager - self.pager_count + 1
                else:
                    pager_start = self.current_page - self.pager_count_half
                    pager_end = self.current_page + self.pager_count_half + 1

        page_html_list = []
        first_page = '<li class="paginate_button page-item"><a href="?page=%s" class="page-link">&lt;&lt;</a></li>' % (1)
        page_html_list.append(first_page)

        if self.current_page <= 1:
            prev_page = '<li id="example1_previous" class="paginate_button page-item previous disabled"><a href="#" class="page-link">&lt;</a></li>'
        else:
            prev_page = '<li id="example1_previous" class="paginate_button page-item previous"><a href="?page=%s" class="page-link">&lt;</a></li>' % (self.current_page - 1,)

        page_html_list.append(prev_page)

        for i in range(pager_start, pager_end):
            if i == self.current_page:
                temp = '<li id="ac_page" name="ac_page" class="paginate_button page-item active"><a href="?page=%s" class="page-link">%s</a></li>' % (i, i,)
            else:
                temp = '<li class="paginate_button page-item"><a href="?page=%s" class="page-link">%s</a></li>' % (i, i,)
            page_html_list.append(temp)

        if self.current_page >= self.all_pager:
            next_page = '<li id="example1_next" class="paginate_button page-item next disabled"><a href="#" class="page-link">&gt;</a></li>'
        else:
            next_page = '<li id="example1_next" class="paginate_button page-item next"><a href="?page=%s" class="page-link">&gt;</a></li>' % (self.current_page + 1,)
        page_html_list.append(next_page)

        last_page = '<li class="paginate_button page-item"><a href="?page=%s" class="page-link">&gt;&gt;</a></li>' % (self.all_pager,)
        page_html_list.append(last_page)
        return ''.join(page_html_list)
