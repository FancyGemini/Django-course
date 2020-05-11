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
