<h1>Backup Reddit Account</h1>

<h3>Info:</h3>
<p>
	With this script you can export all your subreddits. Sometimes you need a new account but want to keep all the subs you follow. Most of the time this is a boring job. 
</p>

<hr>

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
	Rename the <strong>praw.ini.example</strong> to <strong>praw.ini</strong> after that create a Script Reddit app per account. In order to ask the Reddit for data you need an app so use the following link: <a href="https://www.reddit.com/prefs/apps/">https://www.reddit.com/prefs/apps/</a> 
</li>

<li>
Fill a name for the app. The type should be set to script and redirect uri http://localhost:8080 The script will be working locally, no worries for the uri. 
</li>

<li>
	After creating the app we need the credentials. <strong>client_id</strong> is right under the app name and <strong>client_secret</strong> is the secret key. 
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
