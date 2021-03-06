Dgtle-downloader － download images with their origin resolution from www.dgtle.com.

# DESCRIPTION
**Dgtle-downloader** is a command-line program to download images from www.dgtle.com. It requires the Python interpreter, version 3.2+, and it was tested on Windows platform only. It should work on the other platform as well. It is released to the public domain, which means you can modify it, redistribute it or use it however you like.

### What does this program do?

Download multiple original size images at once from a single article page on dgtle.com, and put the images under a folder named by the author's ID.

## How to use it?
### External packages needed
You will need the following packages for this code to work:
* BeautifulSoup
* lxml
* requests

### Step 1
Create an empty folder anywhere on your disk, rename it as you desired.

### Step 2
Open the main page of dgtle.com from your browser.

Shall you find any interested page that you would like to save its origin images from, double click the full URL from the address window to select it, then drag the highlighted selected link into that folder you create on step 1.

### Step 3
By doing the step 2, you will have a url file, called shortcuts that is saved in your folder.

Repeat step 2, until you have had enough urls/shortcuts in your folder.

Make sure the py file and all the URL files are in the same folder. 

To avoid further issues, do not have unnecessary files/folders in that folder.

For example:
```
02/25/2021  11:46 AM    <DIR>          .
02/25/2021  11:46 AM    <DIR>          ..
02/25/2021  11:24 AM             8,076 dgtle.py
02/22/2021  09:23 AM               232 看海看久了想见人，见人见多了想看海.URL
02/20/2021  04:27 PM               232 那一次拍摄：法式优雅.URL
```

### Step 4
Open command line to run dgtle.py from there.

Example:
> D:\dgtle>python dgtle.py 

### Step 5
The folders will be created automatically with the name of each poster's id.

Shall multiple posts share the same author, only one folder will be generated.

For example:
```
02/25/2021  11:24 AM             8,076 dgtle.py
02/25/2021  11:50 AM    <DIR>          小声比比
02/25/2021  11:50 AM    <DIR>          小爺吃面
02/22/2021  09:23 AM               232 看海看久了想见人，见人见多了想看海.URL
02/20/2021  04:27 PM               232 那一次拍摄：法式优雅.URL
```

## Known issues
### Pay extra attention to the page's title.

There is only two valuable pages that comes with pretty images, one named article, the other named intested.

You can tell these two type of pages by looking at their urls that shows as following format:

`https://www.dgtle.com/inst-1693301-1.html`

and 

`https://www.dgtle.com/article-1642352-1.html`

The reason that I do not let this downloader support other pages, is simply because all else pages has no high quality images that worth me to download.

### Download Failed, and Retrying...

Well, as you may see from the code, I tried hard to make sure it keey trying and trying after a highly-possible disconnection happened.

However, certain posters will upload a super large file (more than 30MB), and since the server is located in Beijing, China, the connection quality is terrible for North American users. 

Nothing I could do with that.

### Image saved incomplete

Well, well, well.

This issue has been fixed!

Thanks to the COVID-19, I have plenty of time staying at home, to fix this issue in-side-out.

This is caused by the poor connection.

During transition, if connection flutter, program will consider it MIGHT finished downloading, but it wasn't.

To fix that, I let the download module to check the 'Content-Length' as part of the response.header.

Therefore, if the 'Content-Length' won't match, that means the Internet connection is not reliable. So step back, and try one more time, until we got the correct 'Content-Length'.

This will garantee that the image will be downloaded as a whole piece, and the gray area will never come back again.


## About me

### Why I do this.

I used to enjoy the beautiful photos taken by various photographers all over the world (mainly from China), however, it is painful to save each of them.
Trying to search if there is an existing program available, but with no luck.
So I have to pick up the books and start from zero to build my wheels.

### A little story -- regarding to learning and practice.
It is definitely not the best solution on the Internet, I want to share a story that I learned years ago from a textbook:

Saying the scientist Einstein once in the school, and he had a hard time to build hand crafted objects, and was laughed at by his classmate.
His teacher asked, is there anything worse than this ugly thing?

He nodded his head, and showed him two previous prototypes he had tried earlier.

### That's it, enjoy!
I'm still a beginner in programming, but I believe one day I will be better.

Hope you enjoy the code.

```python
"""
                                   el psy congroo
                                (@&&&&&&&&&&&&&&&&&#                            
                            ,@&&&&&&&&&&&&&&&&&&&&&&&&(,                        
                          %&&&&&&&&&&&&&&&&&&&&&&&&&&&&&(                       
                        ,&&&&&&&&&&&&&&&&&&&&&&&&&&&&@&&&,                      
                        &&&&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&&.                     
                       &&@&&@&&&&&&&&&&&&&@&&&&&&&&&@&&@&&&                     
                      &&@&&&@&&&&&&&&@&&&&@&&&&@&&@&@&&&&&&&                    
                      &&@&&@&@&&&&&&&&&&@&@ &&&@&&@&&&&&@&&@                    
                      @&@&@&%&@&&&&@&&&%@@*@ @@@@@@&@@%&&&&%                    
                      &&&&&% (% @&&&@/&@@.@,///@&&@&@% #&&&&.                   
                       &&@&&,%@@@#&,&(,/.    ,.,&&&&@,,@&&&@*                   
                       &&&@&(#.//(* &          ,&@&&@@&&&&&@@                   
                       &&&&@@@                 &&&&&@&&&&&&@&                   
                        &&&@@@@.               @%&&@&&&&&&@@&(                  
                        (&&@@@@@@     @        @@&&@&&&&&&&&&&                  
                         @&&@@@@@@@@@.      (. &&&@&@&&&&@&@@&@                 
                         &&&@@@@@@@@%@@@%#*#***@&&&&@&&&&&&@@&&@                
                         #&&&@@@@@@@(@@@@#@(%*@&&&&&&&&&&&@@@@&&&#              
                         (&&&&@@@@@,,@@/ %.,@&,FYQ&&&&&&@&@@@@@&&&&@            
                         @&&&&@@@@@@/*%@# /@%@@#MISSISSAUGA@@@@@@&&&&@           
                       ../@,*..   ..*%%% .@%%%&&&ON&CANADA&&,,.,,,,,,@&&          
                    /(,*//*   ,*    /&%%%%%%%(*/(APR 27, 2021*/,*/**&***((,        
                    (%,,%.  /%,     /#%&@@,***,**&&&&@&&&&**,***#**(@%#,,       
                   /,@&,&*,&%,,,.   /%%%%,. .,,*,,(&&&&@&&/*,,**,,&&@&%%.       
                  .#*/%((&(((//*(/ ./%@% %/      */(&&&@&&@(/////@((%(*%,//     
                  @@#..@@@.      ...%#&,# .        ,.&&&@&&,..,,&@@@@@@@.....   
               .(/%///,*/         .#%%@/*  #(//#&%  ,/@&&&&@*//#%@(/%(*,*//,,,  
                &%&(,,((.          &%%**  #        (##(/&&&&,%*%&%%*,,*&&%,,,%  
 """
```
