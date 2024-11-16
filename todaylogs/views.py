from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Today, SelfRecord, Question, Response as UserResponse, AnswerChoice, QuestionType, QuestionSubtype, SurveyCompletion
from .serializers import SelfRecordSerializer, TodaySerializer, TodayDetailSerializer, QuestionSerializer, ResponseSerializer, QuestionSubtypeSerializer, SurveyCompletionSerializer, ResponsesBeforeSerializer
from django.db.models.functions import TruncDate

class TodayListCreateView(generics.ListCreateAPIView):
    serializer_class = TodaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Today.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TodayDetailView(generics.RetrieveAPIView):
    queryset = Today.objects.all()
    serializer_class = TodayDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Today.objects.filter(owner=self.request.user)


class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        question_type = self.request.query_params.get('type', None)
        question_subtype = self.request.query_params.get('subtype', None)
        
        queryset = super().get_queryset()
        
        if question_type:
            queryset = queryset.filter(question_type__type_code=question_type)
        
        if question_subtype:
            queryset = queryset.filter(question_subtype__subtype_code=question_subtype)
        
        return queryset


class ResponseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        today, created = Today.objects.get_or_create(
            owner=request.user,
            created_at__date=timezone.localtime(timezone.now()).date(),
            defaults={'next_appointment_date': None}
        )

        response_type = request.data.get('response_type')  # 'survey' 또는 'side_effect'
        responses = request.data.get('responses')  # 응답 리스트

        if response_type not in ['survey', 'side_effect']:
            return Response({"error": "Invalid response type."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(responses, list):
            return Response({"error": "Responses should be a list."}, status=status.HTTP_400_BAD_REQUEST)

        if not responses:
            return Response({"error": "No responses provided."}, status=status.HTTP_400_BAD_REQUEST)

        subtypes = set()
        for response_data in responses:
            question_id = response_data.get('question_id')
            try:
                question = Question.objects.get(pk=question_id)
                if question.question_subtype:
                    subtypes.add(question.question_subtype)
                else:
                    return Response({"error": "Question subtype is required."}, status=status.HTTP_400_BAD_REQUEST)
            except Question.DoesNotExist:
                return Response({"error": f"Question with id {question_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if len(subtypes) > 1:
            return Response({"error": "All responses must belong to the same subtype."}, status=status.HTTP_400_BAD_REQUEST)

        subtype = subtypes.pop()

        if SurveyCompletion.objects.filter(today=today, response_type=response_type, question_subtype=subtype).exists():
            return Response({"error": "Survey for this subtype has already been completed today."}, status=status.HTTP_400_BAD_REQUEST)

        created_responses = []
        for response_data in responses:
            question_id = response_data.get('question_id')
            answer_id = response_data.get('answer_id')

            try:
                question = Question.objects.get(pk=question_id)
                answer = AnswerChoice.objects.get(pk=answer_id, question_subtype=question.question_subtype)
            except Question.DoesNotExist:
                return Response({"error": f"Question with id {question_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            except AnswerChoice.DoesNotExist:
                return Response({"error": f"AnswerChoice with id {answer_id} does not exist for the question's subtype."}, status=status.HTTP_400_BAD_REQUEST)

            response_instance = UserResponse(
                today=today,
                question=question,
                answer=answer,
                response_type=response_type,
                created_at=timezone.now()
            )
            response_instance.save()
            created_responses.append(response_instance)

        SurveyCompletion.objects.create(
            today=today,
            response_type=response_type,
            question_subtype=subtype,
            completed_at=timezone.now()
        )

        serializer = ResponseSerializer(created_responses, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class SelfRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = SelfRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')

        if not all([year, month, day]):
            return SelfRecord.objects.none()  # 또는 적절한 에러 응답을 반환하도록 수정

        try:
            year = int(year)
            month = int(month)
            day = int(day)
        except ValueError:
            return SelfRecord.objects.none()  # 또는 적절한 에러 응답을 반환하도록 수정

        queryset = SelfRecord.objects.filter(
            today__owner=self.request.user,
            created_at__year=year,
            created_at__month=month,
            created_at__day=day
        )

        return queryset

    def perform_create(self, serializer):
        today, created = Today.objects.get_or_create(
            owner=self.request.user,
            created_at__date=timezone.localtime(timezone.now()).date(),
            defaults={'next_appointment_date': None}
        )
        serializer.save(today=today)


class ResponseListView(generics.ListAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        response_type = self.request.query_params.get('response_type', 'all')  # 'survey', 'side_effect', 또는 'all'

        queryset = UserResponse.objects.filter(
            today__owner=self.request.user,
            today__created_at__year=year,
            today__created_at__month=month,
            today__created_at__day=day
        )

        if response_type in ['survey', 'side_effect']:
            queryset = queryset.filter(response_type=response_type)

        return queryset


class SelfRecordResponseListView(generics.ListAPIView):
    serializer_class = SelfRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')

        return SelfRecord.objects.filter(
            today__owner=self.request.user,
            created_at__year=year,
            created_at__month=month,
            created_at__day=day
        )
        
        
class RecordedDatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year')
        if not year:
            return Response({"error": "Year parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        response_type = request.query_params.get('response_type', 'all')  # 'survey', 'side_effect', 또는 'all'

        queryset = UserResponse.objects.filter(
            today__owner=request.user,
            today__created_at__year=year
        )

        if response_type in ['survey', 'side_effect']:
            queryset = queryset.filter(response_type=response_type)

        dates = queryset.annotate(date=TruncDate('today__created_at')).values_list('date', flat=True).distinct()
        date_strings = [date.isoformat() for date in dates]

        return Response(date_strings)


class SelfRecordRecordedDatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year')
        if not year:
            return Response({"error": "Year parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        dates = SelfRecord.objects.filter(
            today__owner=request.user,
            created_at__year=year
        ).annotate(date=TruncDate('created_at')).values_list('date', flat=True).distinct()

        date_strings = [date.isoformat() for date in dates]

        return Response(date_strings)
    

class QuestionSubtypeListView(generics.ListAPIView):
    serializer_class = QuestionSubtypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        type_code = self.request.query_params.get('type', None)
        queryset = QuestionSubtype.objects.all()

        if type_code:
            queryset = queryset.filter(type__type_code=type_code)

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        response_type = self.request.query_params.get('response_type', 'survey')
        context.update({'response_type': response_type})
        return context
    
class SurveyCompletionListView(generics.ListAPIView):
    serializer_class = SurveyCompletionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = Today.objects.filter(owner=self.request.user, created_at__date=timezone.localtime(timezone.now()).date()).first()
        if not today:
            return SurveyCompletion.objects.none()
        return SurveyCompletion.objects.filter(today=today)
    

class ResponseBeforeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        type_param = request.query_params.get('type', None)
        subtype_code = request.query_params.get('subtype', None)
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)
        day = request.query_params.get('day', None)
        
        if not type_param:
            return Response({"error": "Type 파라미터는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 'type' 파라미터 유효성 검사
        valid_types = dict(UserResponse.RESPONSE_TYPE_CHOICES).keys()
        if type_param not in valid_types:
            return Response({"error": "유효하지 않은 type 파라미터입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if subtype_code:
            # 시나리오 2: 'type'과 'subtype'이 제공된 경우, 날짜 파라미터도 필요
            if not all([year, month, day]):
                return Response({"error": "subtype이 제공된 경우 year, month, day 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            # 날짜 파라미터 유효성 검사 및 변환
            try:
                year = int(year)
                month = int(month)
                day = int(day)
                date_obj = date(year, month, day)
            except ValueError:
                return Response({"error": "유효하지 않은 날짜 파라미터입니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            # 특정 서브타입 가져오기
            try:
                question_subtype = QuestionSubtype.objects.get(
                    subtype_code=subtype_code, 
                    type__type_code=type_param
                )
            except QuestionSubtype.DoesNotExist:
                return Response({"error": "주어진 type에 해당하는 서브타입이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            # 사용자와 날짜에 해당하는 Today 객체 가져오기
            try:
                today = Today.objects.get(owner=request.user, created_at__date=date_obj)
            except Today.DoesNotExist:
                return Response({"error": "해당 날짜에 대한 기록이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
            
            # 해당 조건에 맞는 모든 응답 가져오기
            responses = UserResponse.objects.filter(
                today=today,
                response_type=type_param,
                question__question_subtype=question_subtype
            )
            
            if not responses.exists():
                return Response({"message": "주어진 조건에 맞는 응답이 존재하지 않습니다."}, status=status.HTTP_200_OK)
            
            # 시리얼라이저에 서브타입을 리스트로 전달
            serializer = ResponsesBeforeSerializer(
                {"subtypes": [question_subtype]},
                context={
                    'today': today,
                    'response_type': type_param,
                }
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            # 시나리오 1: 'type'만 제공된 경우, year, month, day 파라미터도 필요
            if not all([year, month, day]):
                return Response({"error": "year, month, day 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            # 날짜 파라미터 유효성 검사 및 변환
            try:
                year = int(year)
                month = int(month)
                day = int(day)
                date_obj = date(year, month, day)
            except ValueError:
                return Response({"error": "유효하지 않은 날짜 파라미터입니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            # 사용자와 날짜에 해당하는 Today 객체 가져오기
            try:
                today = Today.objects.get(owner=request.user, created_at__date=date_obj)
            except Today.DoesNotExist:
                return Response({"error": "해당 날짜에 대한 기록이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
            
            # 주어진 타입에 속하는 모든 서브타입 가져오기
            try:
                question_type = QuestionType.objects.get(type_code=type_param)
            except QuestionType.DoesNotExist:
                return Response({"error": "주어진 type에 해당하는 QuestionType이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            subtypes = QuestionSubtype.objects.filter(type=question_type)
            
            if not subtypes.exists():
                return Response({"message": "주어진 type에 해당하는 서브타입이 존재하지 않습니다."}, status=status.HTTP_200_OK)
            
            # 시리얼라이저에 서브타입을 리스트로 전달
            serializer = ResponsesBeforeSerializer(
                {"subtypes": subtypes},
                context={
                    'today': today,
                    'response_type': type_param,
                }
            )
            return Response(serializer.data, status=status.HTTP_200_OK)