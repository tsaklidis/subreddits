<h1>Backup or Clean Reddit Account</h1>

<h3>Info:</h3>
<p>
	<strong>[Backup]</strong>: With this functinality you can export all your subreddits. Sometimes you need a new account but want to keep all the subs you follow. Most of the time this is a boring job. 
</p>

<p>
	<strong>[Clean]</strong>: With this functinality you can remove all your activity for example delete all the comments you have done or all the posts you have created. People tell personal information that can lead to someone that knows them or recognize them. Lot of people say or posts things in Reddit that in person no one knows. (Actions can't be undone)
</p>

<p>
	<strong>[Confuse]</strong>: Replace your comments and posts text (not title). This is helpfull since deleted comments can still be viewed. Results look like screenshot at the end of page (Actions can't be undone)
</p>

<hr>

<h3>Changelog 2024-01-20:</h3>
<ul>
    <li>Updated to latest praw (7.7.1)</li>
    <li>Under the hood changes for printing messages</li>

</ul>
<h3>Changelog 2020-10-20:</h3>
<ul>
    <li>Ability to select from confusing all data or single (one comment or one single submission)</li>
    <li>Updated to latest praw (7.1.0)</li>
</ul>

<h3>Installation:</h3>

```shell
git clone https://github.com/tsaklidis/subreddits.git
cd subreddits
pip install -r requirements.txt
````

<h3>Prepare:</h3>

<p>

First you need to set the praw.ini file. <br>

<ul>
<li>
	Rename the <strong>praw.ini.example</strong> to <strong>praw.ini</strong> after that create a Reddit app. In order to ask the Reddit for data you need an app so use the following link: <a href="https://www.reddit.com/prefs/apps/">https://www.reddit.com/prefs/apps/</a> 
</li>

<li>
Fill a name for the app. The type should be set to script and redirect uri http://localhost:8080 The script will be working locally, no worries for the uri. 
</li>

<li>
	After createing the app we need the credentials. <strong>client_id</strong> is right under the app name and <strong>client_secret</strong> is the secret key. 
</li>

<li>
Get credentials for old and new accounts. 
</li>

<li>
Fill the data in praw.ini file
</li>
</ul>
</p>



<h3>Use:</h3>
<p>
	Export the subreddits from your old account
</p>

```shell
python3 src/main.py -e
```

<p>
	Import to your new account
</p>

```shell
python3 src/main.py -r
```

<p>
	Export and Import with one run
</p>

```shell
python3 src/main.py -o
```

<hr>

<p>
	<strong>Confuse</strong> all your activity. <i>You will be asked for comments or sumbissions (posts)</i>:
</p>

```shell
python3 src/cleaner.py -c
```

<p>
	<strong>Delete</strong> all your activity. <i>You will be asked for comments or sumbissions (posts)</i>:
</p>

```shell
python3 src/cleaner.py -d
```



![](screens/obf.png)