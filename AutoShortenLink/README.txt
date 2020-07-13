AutoShortenLink
================



Required Python packages
-------------------------



Required Chrome extensions
---------------------------
AdBlock: https://chrome.google.com/webstore/detail/adblock-%E2%80%94-best-ad-blocker/gighmmpiobklfepjocnamgkkbiglidom
Bypass AdBlock Detection: https://chrome.google.com/webstore/detail/bypass-adblock-detection/lppagnomjcaohgkfljlebenbmbdmbkdj/related


How do captchas work?
----------------------
- How does I'M NOT A ROBOT captcha work (No-Captcha Recaptcha)?
    This method tracks the movement and figures.
    Bots are more likely to check the box right in the middle while and in very short duration,
    while humans tend to click in some other areas of the box.

    It is incredibly effective and accurate.
    However, as the first test fails, there is another test requiring users to choose all the related images 
    from the following section or type some combinations of numbers or letters.

- How does Invisible Recaptcha work?
    This is an updated version of No-Captcha Recaptcha. It is completely invisible to the users. 
    Therefore, the users don’t need to tick the box, enter the text, match the images or fill out the form.

    It involves monitoring the way users interact with the website, 
    how they click on an existing button, how they move the mouse and other behaviors selected and analyzed by Google.


How to pass captchas
---------------------
- Slow down the script
    Captcha can record the amount of time that users spend to complete the form.
    Bots tend to fill out the form immediately while humans will take a bit of time.
   -> Use time gap between requests. Use time.sleep() to delay consecutive requests. Usually a time delay of 2 seconds would be enough.
   
- Simulate mouse movement like human: https://www.dreamincode.net/forums/topic/404519-python-pyautogui-human-like-mouse-movement/

- Change user agent: https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/computer/8

- Use selenium only and set a proper window screen size. Most modern web apps identify users based on window size.
In your case it is not recommended going for other solutions such as requests which do not allow proper handling of window size.

- Keep chaining and changing proxies with each interval of xxx requests (depends upon your work load).

- Use a modern valid user agent (Mozilla 5.0 compatible). Usually a Chrome browser > 60.0 UA will work good.

- Use a single user agent for a specific proxy. If your UA keeps changing for a specific IP, Recaptcha will grab you as automated.

- Handle cookies properly. Make sure the cookies set by the server are sent with subsequent requests (for a single proxy).


How to prevent Selenium detection?
-----------------------------------
https://stackoverflow.com/a/53040904
https://stackoverflow.com/a/61630569

** Chrome headless: https://intoli.com/blog/not-possible-to-block-chrome-headless/    (not tried yet)
                    https://github.com/paulirish/headless-cat-n-mouse   (not tried yet)

How to pass "Your computer or network may be sending automated queries..."
----------------------------------------------------------------------------
Cause: by Buster extension
https://github.com/dessant/buster/issues/56#issuecomment-481655521


These ways work:
First: https://www.youtube.com/watch?v=aVqvo7q0DAA

These ways do not work:
- Change profile
- Change user agent
- Change IP address




