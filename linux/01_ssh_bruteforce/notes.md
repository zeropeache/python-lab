to start I made a cron for my project, considering my device i thought it would  be a good idea
to back up my device. I used a simple 12 hour loop. My first step is to look into this auth.log from a Linux server. 
The (fictional) security team from Osiris&Co suspects someone is brute-forcing SSH logins. 

So my job is to write a Python script that parses auth.log and extracts failed SSH login attempts, as well as counting failures per IP addresse which I ca flag any IP that exceeds a threshold (e.g. 5 failures).
Then it will print a clean report of everything: flagged IPs, failure counts, and the usernames that were targeted. 

To really start I had to do some research to remind myself important steps in this type of incident. I have an Obsidian vault with all my notes from studying and applying my skills. So after consulting a few notes I had to ask myself a few questions:
WHat type of failed login lines stand out as useful?

Is there a correlating IP address?

Is there any other type of failed messaged or just the one pattern?

I am used a generated auth.log, so what would break in my code if it was bigger than 10GB?

Is my code ready to flag the same IP if it appears in both "Failed" and "Invalid line"?



So I played around with making the script, tested it, failed, fixed it, next synthax error (putting a s where a s shoulkd not be). Lots of imperfections.

I initially wanted to use a break expect, but I didnt filter any errors through so I was just giving it a chance to say nothing, wouldnt be able to fix anything if it doesnt say anything. So I removed it. I could "except '.error'" something...

I had a few typos, had to go through my notes on regex and a forum to include it, much better than a dot-counting method...
I also had to catch up on lambda.

My script works, it gives out the excpected output and could use more polishing. I am going to try new auth.logs to see if it can adapt.
 
