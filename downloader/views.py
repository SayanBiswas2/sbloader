from django.shortcuts import render,HttpResponse,redirect
from pytube import YouTube
import os
import time
import subprocess 

def timec(time):
  H= 0
  m= 0
  s= 0
  if time>3600:
    H= time/3600
    m= (time%3600)/60
    s= time%60
  else:
    m= time/60
    s= time%60
  time= str(int(H))+":"+str(int(m))+':'+str(int(s))
  return time
def home(request):
  filelist= os.listdir('./static/DB')
  print(filelist)
  for i in filelist:
    c_time= os.path.getctime('./static/DB/'+i)
    times= time.time()
    if (c_time-times)< -600:
      print('removing:'+i)
      os.remove('./static/DB/'+i)
  return render(request,'index.html')

def ythome(request):
  #return render(request,'youtube.html')
  if request.method == 'GET':
    try:
      first= request.GET['first']
    except:
      first= True
    print(first)
    if first == True:
      return render(request,'youtube.html')
    else:
      try:
        link= request.GET['link']
        video= YouTube(link)
        thum= video.thumbnail_url
        title= "title:"+video.title
        length=video.length
        length= "Duration: " +timec(length)
        res= []
        strmall= video.streams.all()
        print('ok')
        for i in strmall:
          res.append(i.resolution)
        res = list(set(res))
        data= {
        'a': 1,
        'thum':thum,
        'title':title,
        'len':length,
        'res':res,
        'url':link,
        }
        return render(request,'youtube.html',data)
      except Exception as e:
        print(e)
        return render(request,'youtube.html',{'err':'error'})
    return render(request,'youtube.html')
        
  if request.method == 'POST':
    link=request.POST['link']
    rsl= request.POST['res']
    csrf= request.POST['csrfmiddlewaretoken']
    csrfl=csrf+".mp4"
    video = YouTube(link)
    title=video.title
    try:
      stream= video.streams.filter(res=rsl, progressive= True).first()
      stream.download('./static/DB' ,filename= csrfl)
    except:
      stream= video.streams.filter(res=rsl).first()
      stream.download('./static/DB' , filename=csrfl)
      stream= video.streams.filter(only_audio= True).first()
      file=csrf+".mp3"
      stream.download('./static/DB' ,filename= file)
      videofile= './static/DB/'+csrfl
      audiofile= './static/DB/'+file
      os.system(f'ffmpeg -i {videofile} -i {audiofile} -map 0:v -map 1:a -c:v copy -c:a copy video.mp4 -y')
      csrfl=csrf+'.mkv'
      
    video={
      'filename':csrfl,
      'name':title
    }
    return render(request,'youtube.html',video)

def instagram(request):
  if request.method=='GET':
    try:
      print('ok!')
      link= request.GET['link']
      csrf= request.GET['csrfmiddlewaretoken']
      
      insta_reel = Reel(link)
      print(link)
      SESSIONID = "12345678901%3Aabcdefghijkl1a%3A2"
      """
      headers = {
      "User-Agent": "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74"
      
      #Safari/537.36 Edg/79.0.309.43",
        
     # "cookie": (f'sessionid={SESSIONID};')
      }"""
      print(csrf)
      insta_reel.download(fp="/static/DB/"+csrf+".mp4")
      print('ok3!')
      print('Downloaded Successfully.')
      file=csrf+'.mp4'
      data={
        'filename':file,
        
      }
      return render(request,'instagram.html',data)
    except Exception as e:
      print(e)
      return render(request,'instagram.html')



def download(request):
  if request.method == 'POST':
    link=request.POST['link']
    rsl= request.POST['res']
    csrf= request.POST['csrfmiddlewaretoken']
    csrfl=csrf+".mp4"
    video = YouTube(link)
    title=video.title
    try:
      stream= video.streams.filter(res=rsl, progressive= True).first()
      stream.download('./static/DB' ,filename= csrfl)
    except:
      stream= video.streams.filter(res=rsl).first()
      stream.download('./static/DB' , filename=csrfl)
      stream= video.streams.filter(only_audio= True).first()
      file=csrf+".mp3"
      stream.download('./static/DB' ,filename= file)
      videofile= './static/DB/'+csrfl
      audiofile= './static/DB/'+file
      os.system(f'ffmpeg -i {videofile} -i {audiofile} -map 0:v -map 1:a -c:v copy -c:a copy video.mp4 -y')
      csrfl=csrf+'.mkv'
    return render(request,'download.html',{'filename':csrfl,'name':title})
  return render(request,'index.html')
def terms(request):
  return render(request,'terms.html')
  

def app(request):
  return render(request,'getapp.html')