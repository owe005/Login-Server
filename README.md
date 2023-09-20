# INF 226 - Assignment 02 - Ole Kristian Westby AKA owe009.

## Part 2A:

### Initial code structure

The state that the project is in at the start of this assignment is really badly structured. It is messy. This is a problem because it makes it harder to spot potential bugs, loopholes, security flaws, etc.. I'm a huge fan of keeping import statements at the top, grouped up so that it is easy to see what requirements are needed/used for the project. (As long as doable regarding circular dependencies). When it is as messy and unstructured as it is, one solution could be to split the code into multiple files (but keep related code grouped).

### Security issues
First of all, it took me 10 seconds to figure out the secret key for the encrypted session data from Flask. This is because it was directly stored in the source code. You can easily solve this by using system environment variables. This way you can store it separately from the source code but still be able to refer to it without it being leaked.

Then I saw that the usernames and passwords of all the available users was in the source code posing a BIG security issue for those users. (As well as their passwords not being particularly strong).
I attempted to send a message logged in as Alice, and since the source code contains the database for messages and announcements, I was also able to see all messages sent, posing a privacy issue.

Additionally, there is no check to see if the password provided for the corresponding username is correct, meaning all you need to log in is the username. You can also change your name to someone else and send a message from that username, with absolutely no challenges. (Imposter!)

### Changes
The first thing I did was decide to group up relevant code in their own separate python files and then import them where needed. Example of this is the login() function. (And later on the register() function. Both large code snippets that are better of being separate.

- ✅removed the "feature" of being able to change your name to any user and then be that user.
- ✅added a way for new users to register.
- ✅you can now logout!
- ✅passwords are checked against login details.
- ✅passwords are hashed and not available in the source code.
- ✅announcements is effectively obsolete (wasn't sure what to do with it.)
- ✅salt and password hash stored in database.
- ✅messages technically don't have a timestamp in the database but I half-assed a way for timestamps to appear through the time library.

### Future plans if I had more time.
- ❌add a way to block other users
- ❌1/2 add another url that the user goes to first before the login screen.
- ❌2/2 then add a captcha to avoid spam bots (pests on chat software)
- ❌make the UI more user friendly
- ❌sound sfx for messages?
- ❌profiles for users (profile pictures? (upload their own?))
- ❌and more!

### How 2 Run
- pip install flask + **other requirements**
- flask run
- localhost:5000 or http://127.0.0.1:5000
- chat away.

## Part 2B:

### Questions
- Threat model – who might attack the application?<br/>
<b>As this is a messaging app, it would make sense that a potential attacker could be after confidential information. With *little work* in it's starting stage an attacker could pretend to be another user, delete/edit already sent messages and gain access to sensitive information. The current users have VERY weak passwords which suggests that they might be using these passwords elsewhere, therefore an attacker could use this information elsewhere.</b>

- What can an attacker do? What damage could be done (in terms of confidentiality, integrity, availability)? Are there limits to what an attacker can do? Are there limits to what we can sensibly protect against?<br/>
<b>With confidentiality, integrity and availability in mind there are many different ways for an attacker to exploit the security issues of the application in the beginning.</b>

    *Confidentiality*<br/>
    <b>There is no password check. Anyone could login to any user without even having the corresponding password, thus being able to read anyone's messages.</b><br/>
    *Integrity*<br/>
    <b>An attacker could send messages pretending to be other users, or forge a message in the database, for example through an SQL injection.</b><br/>
    *Availability*<br/>
    <b>By doing an SQL injection, an attacker can delete messages. Alternatively, an attacker could bring the service to a halt with a DoS/DDos attack.</b><br/>

- What are the main attack vectors for the application?<br/>
<b>For one if my users don't have strong passwords, that could become a problem. A way to fix this is to have requirements on passwords, e.g min. 6 char length and 1 capital letter.. etc.. but I haven't implemented that yet! Since it's a chatting software, phishing is a common attack vector. DDos. </b>

- What should we do (or what have you done) to protect against attacks?<br/>
<b>For one I have removed the "feature" of being able to change your name to any user and then be that user. This to avoid phishing attacks, or impersonation. Passwords are checked against login details. Passwords are hashed and not available in the source code. SQL injections are limited. </b>

- What is the access control model?<br/>
<b>I think a mix of "enforce least privileges" and "deny by default". Without logging in there isn't anything that the user is able to do except registering. The user is also quite limited on what he/she is able to do once logged in. </b>

- How can you know that you security is good enough? (traceability)<br/>
<b>There are constantly new ways being discovered that can threaten security. I think if you keep up with the latest tricks, methods, technology and ways to protect yourself against attacks, that is a good way to protect your application. I don't think security will ever be "good enough", especially when attackers find new ways every day. That's my answer, you cant. You won't be able to know if it's good enough until someone actually attacks your application, in which it's already too late.</b>

![what could'of been..](/image/soon.jpg "CatsChat")

###### CatsChatTM.. soon a reality.. for now just a dream..
