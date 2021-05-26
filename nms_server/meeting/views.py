import logging
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from nms_server.dao.meeting import *
from nms_server.utils import error_code

logger = logging.getLogger("nms." + __name__)

# -----------------------------实时会议功能函数-----------------------------------
# 点对点会议列表
class RealTimeP2pMeeting(APIView):
    def get(self, request, *args, **kwargs):
        
        page = request.GET.get('page')
        parentMoid = request.GET.get('parentMoid')
        meetingName = request.GET.get('meetingName')

        if parentMoid == None or meetingName == None or page == None:
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if parentMoid == 'all':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info('[RealTimeP2pMeeting] parentMoid=%s' % parentMoid)
        logger.info('[RealTimeP2pMeeting] meetingName=%s' % meetingName)
        logger.info('[RealTimeP2pMeeting] page=%s' % page)

        response = {'success': 1}
        response['data'], response['total_num'] = get_realtime_p2p_meeting(parentMoid, page, meetingName)
        return Response(response)

# 会议终端详情
class RealTimeTerminalDetail(APIView):
    def get(self, request, *args, **kwargs):
        
        terminalE164 = request.GET.get('terminalE164')
        if terminalE164 == None or terminalE164 == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[RealTimeTerminalDetail] terminalE164=%s' % terminalE164)

        response = {'success': 1}
        response['data'] = get_realtime_terminal_detail(terminalE164)
        return Response(response)

# 会议终端主辅视频信息
class RealTimeTerminalVideoDetail(APIView):
    def get(self, request, *args, **kwargs):
        
        terminalE164 = request.GET.get('terminalE164')
        if terminalE164 == None or terminalE164 == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[RealTimeTerminalVideoDetail] terminalE164=%s' % terminalE164)

        response = {'success': 1}
        response['PrivideoData'] = get_realtime_terminal_privideo(terminalE164)
        response['AssvideoData'] = get_realtime_terminal_assvideo(terminalE164)
        return Response(response)

# 多点会议列表
class RealTimeMultiMeeting(APIView):
    def get(self, request, *args, **kwargs):
        
        page = request.GET.get('page')
        parentMoid = request.GET.get('parentMoid')
        meetingName = request.GET.get('meetingName')

        if parentMoid == None or meetingName == None or page == None:
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if parentMoid == 'all':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info('[RealTimeMultiMeeting] parentMoid=%s' % parentMoid)
        logger.info('[RealTimeMultiMeeting] meetingName=%s' % meetingName)
        logger.info('[RealTimeMultiMeeting] page=%s' % page)

        response = {'success': 1}
        response['data'], response['total_num'] = get_realtime_multi_meeting(parentMoid, page, meetingName)
        return Response(response)

# 多点会议详情
class RealTimeMultiMeetingDetail(APIView):
    def get(self, request, *args, **kwargs):

        meetingE164 = request.GET.get('meetingE164')
        meetingType = request.GET.get('meetingType')
        if meetingE164 == None or meetingE164 == '' or meetingType == None or meetingType == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[RealTimeMultiMeetingDetail] meetingE164=%s' % meetingE164)
        logger.info('[RealTimeMultiMeetingDetail] meetingType=%s' % meetingType)

        response = {'success': 1}
        response['data'] = get_realtime_multi_meeting_detail(meetingE164,meetingType)
        return Response(response)

# 软硬终端列表
class RealTimeSoftHardTerminal(APIView):
    def get(self, request, *args, **kwargs):
        
        page = request.GET.get('page')
        meetingE164 = request.GET.get('meetingE164')
        terminalName = request.GET.get('terminalName')

        if meetingE164 == None or meetingE164 == '' or page == None or page == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if terminalName == None:
            terminalName = ''

        logger.info('[RealTimeSoftHardTerminal] meetingE164=%s' % meetingE164)
        logger.info('[RealTimeSoftHardTerminal] terminalName=%s' % terminalName)
        logger.info('[RealTimeSoftHardTerminal] page=%s' % page)
        response = {'success': 1}
        response['data'], response['total_num'] = get_realtime_softhard_terminal(meetingE164, page, terminalName)
        return Response(response)

# 终端入离会信息列表
class RealTimeTerminalLeaveReason(APIView):
    def get(self, request, *args, **kwargs):
        meetingE164 = request.GET.get('meetingE164')
        terminalMoid = request.GET.get('terminalMoid')
        if meetingE164 == None or meetingE164 == '' or terminalMoid == None or terminalMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[RealTimeTerminalLeaveReason] meetingE164=%s' % meetingE164)
        logger.info('[RealTimeTerminalLeaveReason] terminalMoid=%s' % terminalMoid)

        response = {'success': 1}
        response['data'] = get_realtime_terminal_leave_reason(meetingE164, terminalMoid)
        return Response(response)


# 终端参会概况列表
class RealTimeTerminalMeetingScore(APIView):
    def get(self, request, *args, **kwargs):
        meetingE164 = request.GET.get('meetingE164')
        terminalMoid = request.GET.get('terminalMoid')
        if meetingE164 == None or meetingE164 == '' or terminalMoid == None or terminalMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[RealTimeTerminalMeetingScore] meetingE164=%s' % meetingE164)
        logger.info('[RealTimeTerminalMeetingScore] terminalMoid=%s' % terminalMoid)

        response = {'success': 1}
        response['data'] = get_realtime_terminal_meeting_score(meetingE164, terminalMoid)
        return Response(response)


# 电话终端列表
class RealTimePhoneTerminal(APIView):
    def get(self, request, *args, **kwargs):

        page = request.GET.get('page')
        meetingE164 = request.GET.get('meetingE164')
        terminalName = request.GET.get('terminalName')

        if meetingE164 == None or meetingE164 == '' or page == None or page == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if terminalName == None:
            terminalName = ''

        logger.info('[RealTimePhoneTerminal] meetingE164=%s' % meetingE164)
        logger.info('[RealTimePhoneTerminal] terminalName=%s' % terminalName)
        logger.info('[RealTimePhoneTerminal] page=%s' % page)

        response = {'success': 1}
        response['data'], response['total_num'] = get_realtime_phone_terminal(meetingE164, page, terminalName)
        return Response(response)

# 级联会议
class RealTimeCascadeMeeting(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        meetingE164 = request.GET.get('meetingE164')
        meetingName = request.GET.get('meetingName')

        if meetingE164 == None or meetingE164 == '' or page == None or page == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if meetingName == None:
            meetingName = ''

        logger.info('[RealTimeCascadeMeeting] meetingE164=%s' % meetingE164)
        logger.info('[RealTimeCascadeMeeting] meetingName=%s' % meetingName)
        logger.info('[RealTimeCascadeMeeting] page=%s' % page)

        response = {'success': 1}
        response['data'], response['total_num'] = get_realtime_cascade_meeting(meetingE164, page, meetingName)
        return Response(response)

# IP和友商终端列表
class RealTimeIPTerminal(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        meetingE164 = request.GET.get('meetingE164')
        terminalName = request.GET.get('terminalName')

        if meetingE164 == None or meetingE164 == '' or page == None or page == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if terminalName == None:
            terminalName = ''

        logger.info('[RealTimeIPTerminal] meetingE164=%s' % meetingE164)
        logger.info('[RealTimeIPTerminal] terminalName=%s' % terminalName)
        logger.info('[RealTimeIPTerminal] page=%s' % page)

        response = {'success': 1}
        response['data'], response['total_num'] = get_realtime_ip_terminal(meetingE164, page, terminalName)
        return Response(response)

# 直播列表
class RealTimeLiveInfo(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        meetingE164 = request.GET.get('meetingE164')

        if meetingE164 == None or meetingE164 == '' or page == None or page == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[RealTimeLiveInfo] meetingE164=%s' % meetingE164)
        logger.info('[RealTimeLiveInfo] page : %s' % page)

        response = {'success': 1}
        response['data'] = get_realtime_live_info(meetingE164,page)
        return Response(response)

# 数据会议信息
class RealTimeDcsInfo(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        meetingE164 = request.GET.get('meetingE164')
        coopState = request.GET.get('coopState')
        if meetingE164 == None or meetingE164 == '' or coopState == None or coopState == '' or page == None or page == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[RealTimeMeetingDcsInfo] meetingE164 : %s' % meetingE164)
        logger.info('[RealTimeMeetingDcsInfo] coopState : %s' % coopState)
        logger.info('[RealTimeMeetingDcsInfo] page : %s' % page)

        response = {'success': 1}
        response['data'] = get_realtime_dcs_info(meetingE164,coopState,page)
        return Response(response)

# -----------------------------历史会议功能函数-----------------------------------
# 点对点会议列表
class HistoryP2pMeeting(APIView):
    def get(self, request, *args, **kwargs):
        
        page = request.GET.get('page')
        parentMoid = request.GET.get('parentMoid')
        meetingName = request.GET.get('meetingName')

        if parentMoid == None or meetingName == None or page == None:
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if parentMoid == 'all':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info('[HistoryP2pMeeting] parentMoid=%s' % parentMoid)
        logger.info('[HistoryP2pMeeting] meetingName=%s' % meetingName)
        logger.info('[HistoryP2pMeeting] page=%s' % page)

        response = {'success': 1}
        response['data'], response['total_num'] = get_history_p2p_meeting(parentMoid, page, meetingName)
        return Response(response)

# 点对点会议详情列表(主叫信息)
class HistoryP2pMeetingDetail(APIView):
    def get(self, request, *args, **kwargs):
        
        meetingMoid = request.GET.get('meetingMoid')
        if meetingMoid == None or meetingMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[HistoryP2pMeetingDetail] meetingMoid=%s' % meetingMoid)

        response = {'success': 1}
        response['data'] = get_history_p2p_meeting_detail(meetingMoid)
        return Response(response)

# 点对点会议详情列表(被叫信息)
class HistoryP2pMeetingCallee(APIView):
    def get(self, request, *args, **kwargs):

        meetingMoid = request.GET.get('meetingMoid')
        if meetingMoid == None or meetingMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[HistoryP2pMeetingCallee] meetingMoid=%s' % meetingMoid)

        response = {'success': 1}
        response['data'] = get_history_p2p_meeting_callee(meetingMoid)
        return Response(response)

# 点对点会议主辅视频信息
class HistoryP2pMeetingVideo(APIView):
    def get(self, request, *args, **kwargs):
        
        meetingMoid = request.GET.get('meetingMoid')
        terminalMoid = request.GET.get('terminalMoid')
        if meetingMoid == None or meetingMoid == '' or terminalMoid == None or terminalMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[HistoryP2pMeetingVideo] meetingMoid=%s' % meetingMoid)
        logger.info('[HistoryP2pMeetingVideo] terminalMoid=%s' % terminalMoid)

        response = {'success': 1}
        response['PrivideoData'] = get_history_p2p_privideo(meetingMoid, terminalMoid)
        response['AssvideoData'] = get_history_p2p_assvideo(meetingMoid, terminalMoid)
        return Response(response)

# 多点会议列表
class HistoryMultiMeeting(APIView):
    def get(self, request, *args, **kwargs):
        
        page = request.GET.get('page')
        parentMoid = request.GET.get('parentMoid')
        meetingName = request.GET.get('meetingName')

        if parentMoid == None or meetingName == None or page == None:
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if parentMoid == 'all':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info('[HistoryMultiMeeting] parentMoid=%s' % parentMoid)
        logger.info('[HistoryMultiMeeting] meetingName=%s' % meetingName)
        logger.info('[HistoryMultiMeeting] page=%s' % page)

        response = {'success': 1}
        response['data'], response['total_num'] = get_history_multi_meeting(parentMoid, page, meetingName)
        return Response(response)

# 多点会议详情
class HistoryMultiMeetingDetail(APIView):
    def get(self, request, *args, **kwargs):

        meetingMoid = request.GET.get('meetingMoid')
        if meetingMoid == None or meetingMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[HistoryMultiMeetingDetail] meetingMoid=%s' % meetingMoid)

        response = {'success': 1}
        response['data'] = get_history_multi_meeting_detail(meetingMoid)
        return Response(response)

# 软硬终端列表
class HistorySoftHardTerminal(APIView):
    def get(self, request, *args, **kwargs):
        
        page = request.GET.get('page')
        meetingMoid = request.GET.get('meetingMoid')
        terminalName = request.GET.get('terminalName')

        if meetingMoid == None or meetingMoid == '' or page == None or page == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if terminalName == None:
            terminalName = ''

        logger.info('[HistorySoftHardTerminal] meetingMoid=%s' % meetingMoid)
        logger.info('[HistorySoftHardTerminal] terminalName=%s' % terminalName)
        logger.info('[HistorySoftHardTerminal] page=%s' % page)
        response = {'success': 1}
        response['data'], response['total_num'] = get_history_softhard_terminal(meetingMoid, page, terminalName)
        return Response(response)

# 软硬终端详情
class HistorySoftHardTerminalDetail(APIView):
    def get(self, request, *args, **kwargs):

        meetingMoid = request.GET.get('meetingMoid')
        terminalMoid = request.GET.get('terminalMoid')
        if meetingMoid == None or meetingMoid == '' or terminalMoid == None or terminalMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[HistorySoftHardTerminalDetail] meetingMoid=%s' % meetingMoid)
        logger.info('[HistorySoftHardTerminalDetail] terminalMoid=%s' % terminalMoid)

        response = {'success': 1}
        response['data'] = get_history_softhard_terminal_detail(meetingMoid, terminalMoid)
        return Response(response)

# 终端入离会原因
class HistoryTerminalLeaveReason(APIView):
    def get(self, request, *args, **kwargs):
        meetingMoid = request.GET.get('meetingMoid')
        terminalMoid = request.GET.get('terminalMoid')

        if meetingMoid == None or meetingMoid == '' or terminalMoid == None or terminalMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[HistoryTerminalLeaveReason] meetingMoid=%s' % meetingMoid)
        logger.info('[HistoryTerminalLeaveReason] terminalMoid=%s' % terminalMoid)

        response = {'success': 1}
        response['data'] = get_history_terminal_leave_reason(meetingMoid, terminalMoid)
        return Response(response)


# 终端参会概况
class HistoryTerminalMeetingScore(APIView):
    def get(self, request, *args, **kwargs):
        meetingMoid = request.GET.get('meetingMoid')
        terminalMoid = request.GET.get('terminalMoid')

        if meetingMoid == None or meetingMoid == '' or terminalMoid == None or terminalMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[HistoryTerminalLeaveScore] meetingMoid=%s' % meetingMoid)
        logger.info('[HistoryTerminalLeaveScore] terminalMoid=%s' % terminalMoid)

        response = {'success': 1}
        response['data'] = get_history_terminal_meeting_score(meetingMoid, terminalMoid)
        return Response(response)


# 电话终端
class HistoryPhoneTerminal(APIView):
    def get(self, request, *args, **kwargs):

        page = request.GET.get('page')
        meetingMoid = request.GET.get('meetingMoid')
        terminalName = request.GET.get('terminalName')

        if meetingMoid == None or meetingMoid == '' or page == None or page == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if terminalName == None:
            terminalName = ''

        logger.info('[HistoryPhoneTerminal] meetingMoid=%s' % meetingMoid)
        logger.info('[HistoryPhoneTerminal] terminalName=%s' % terminalName)
        logger.info('[HistoryPhoneTerminal] page=%s' % page)

        response = {'success': 1}
        response['data'], response['total_num'] = get_history_phone_terminal(meetingMoid, page, terminalName)
        return Response(response)

# 级联会议
class HistoryCascadeMeeting(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        meetingMoid = request.GET.get('meetingMoid')
        meetingName = request.GET.get('meetingName')

        if meetingMoid == None or meetingMoid == '' or page == None or page == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if meetingName == None:
            meetingName = ''

        logger.info('[HistoryCascadeMeeting] meetingMoid=%s' % meetingMoid)
        logger.info('[HistoryCascadeMeeting] meetingName=%s' % meetingName)
        logger.info('[HistoryCascadeMeeting] page=%s' % page)

        response = {'success': 1}
        response['data'], response['total_num'] = get_history_cascade_meeting(meetingMoid, page, meetingName)
        return Response(response)

# ip和友商终端
class HistoryIPTerminal(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        meetingMoid = request.GET.get('meetingMoid')
        terminalName = request.GET.get('terminalName')

        if meetingMoid == None or meetingMoid == '' or page == None or page == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if terminalName == None:
            terminalName = ''

        logger.info('[HistoryIPTerminal] meetingMoid=%s' % meetingMoid)
        logger.info('[HistoryIPTerminal] terminalName=%s' % terminalName)
        logger.info('[HistoryIPTerminal] page=%s' % page)

        response = {'success': 1}
        response['data'], response['total_num'] = get_history_ip_terminal(meetingMoid, page, terminalName)
        return Response(response)

# 直播列表
class HistoryLiveInfo(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        meetingMoid = request.GET.get('meetingMoid')

        if meetingMoid == None or meetingMoid == '' or page == None or page == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[HistoryLiveInfo] meetingMoid=%s' % meetingMoid)
        logger.info('[HistoryLiveInfo] page=%s' % page)

        response = {'success': 1}
        response['data'], response['total_num'] = get_history_live_info(meetingMoid, page)
        return Response(response)

# 直播用户列表
class HistoryLiveUserInfo(APIView):
    def get(self, request, *args, **kwargs):

        liveMoid = request.GET.get('liveMoid')
        if liveMoid == None or liveMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[HistoryLiveUserInfo] liveMoid=%s' % liveMoid)

        response = {'success': 1}
        response['data'] = get_history_live_user_info(liveMoid)
        return Response(response)

# 数据会议信息（包含点对点和多点）
class HistoryMeetingDcsInfo(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        meetingMoid = request.GET.get('meetingMoid')
        if meetingMoid == None or meetingMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[HistoryMeetingDcsInfo] meetingMoid : %s' % meetingMoid)

        response = {'success': 1}
        response['data'], response['total_num'] = get_history_meeting_dcs_info(meetingMoid, page)
        return Response(response)

# 数据会议模式变更记录
class HistoryDcsModeChangeInfo(APIView):
    def get(self, request, *args, **kwargs):
        
        dcsMoid = request.GET.get('dcsMoid')
        if dcsMoid == None or dcsMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[HistoryDcsModeChangeInfo] dcsMoid : %s' % dcsMoid)

        response = {'success': 1}
        response['data'] = get_history_dcs_mode_change_info(dcsMoid)
        return Response(response)


# 数据会议终端信息
class HistoryDcsMeetingTerminal(APIView):
    def get(self, request, *args, **kwargs):

        dcsMoid = request.GET.get('dcsMoid')
        if dcsMoid == None or dcsMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[HistoryDcsMeetingTerminal] dcsMoid : %s' % dcsMoid)

        response = {'success': 1}
        response['Collaborator'], response['Viewer'] = get_history_dcs_meeting_terminal(dcsMoid)
        return Response(response)