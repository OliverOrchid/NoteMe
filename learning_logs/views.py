# from .models import Topic

####################################
# Create your views here.(即：编写视图)
#视图函数接受请求中的信息，准备好生成网页所需的数据，再将这些数据发送给浏览器——这通常是使用定义了网页是什么样的模板实现的
#####################################

from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required#术语:"装饰器"


from .models import Topic,Entry
from .forms import TopicForm,EntryForm

def index(request):#request 是由浏览器所发出的请求,称作“请求对象”，浏览器能够发出多种请求，详见百科
    """
    学习笔记的主页
    """
    return render(request, 'learning_logs/index.html' )


#######################################
def check_topic_owner(request,topic):
    if request.user != topic.owner:
        return True




#######################################



@login_required
def topics(request):
    """显示所有的主题 """

    topics= Topic.objects.filter(owner = request.user).order_by('date_added')
    
    context= {'topics':topics}
    return render(request,'learning_logs/topics.html'
        ,context)

@login_required
def topic(request,topic_id):
	"""显示单个主题及其所有的条目"""
	topic=Topic.objects.get(id=topic_id)
	if  check_topic_owner(request,topic):
		raise   Http404
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic,'entries':entries}
	return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    """
    添加新主题
    """
    if request.method != 'POST':
        #若未提交(即：POST)数据则创建新表格
        form = TopicForm()#L13 ，实参为空 故而 返回一个空表单
    else:
        #若POST数据，则对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            form.save()
            return HttpResponseRedirect(
                reverse('learning_logs:topics')
                )

    context = {'form':form}#context 称作“上下文对象”
    return render(request,'learning_logs/new_topic.html'
        ,context)

@login_required
def new_entry(request,topic_id):
    """
        在特定的主题中添加新条目
    """
    #topic = Topic.objects.get(id=topic_id)
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()

    else:
        form = EntryForm(data = request.POST)
        if form.is_valid():

            ########  BYOLIVER  ###########
            if check_topic_owner(request,topic):
                raise Http404
            #######################

            new_entry = form.save(commit = False)#L71 与topic共同存储到数据库中
            new_entry.topic = topic
            new_entry.save()#commit默认为True
            return HttpResponseRedirect(
                reverse('learning_logs:topic',
                    args = [topic_id])
                )

    context = {'topic':topic,'form':form}
    return render(request , 'learning_logs/new_entry.html'
        ,context
        )

@login_required
def edit_entry(request,entry_id):
    """
        编辑既有条目
    """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # if topic.owner != request.user:
    #   raise Http404
    if  check_topic_owner(request,topic):
        raise Http404

    if request.method != 'POST':
        #若首次请求，则使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        #若 非首次请求（即为POST请求） ， 则 对用户提交的数据进行处理
        form = EntryForm(instance=entry,data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))


    context = {'entry':entry,'topic':topic,'form':form}

    return render(request,'learning_logs/edit_entry.html',context)

####END!!!!


