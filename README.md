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
Currently, this code is semi-auto, and it is designed to work with any url that shows as following format:

`https://www.dgtle.com/inst-1693301-1.html`

and 

`https://www.dgtle.com/article-1642352-1.html`

Any other pages that contain a video or those post dates earlier than 2014, this code might not work properly.

### Download Failed, and Retrying...
Certain posters will upload a super large file (more than 30MB), and since the server is located in Beijing, China, the connection quality is terrible for North American users.

### Image saved incomplete
Due to the poor connection, the image that was downloaded might be incomplete. Which you might see a grey area at the lower section of that image.

#### Temporary solution:
* Retry the download one more time. 
* Try it at a later time.
* Delete this image if you are not pleased.
* Go to the page and save it manually.


## About me

### Why I do this.

I used to enjoy the beautiful photos taken by various photographers all over the world (mainly from CHina), however, it is painful to save each of them.
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
