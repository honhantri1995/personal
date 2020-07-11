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

- Change user agent: https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/computer/8

How to prevent Selenium detection?
-----------------------------------
https://stackoverflow.com/a/53040904
https://stackoverflow.com/a/61630569

** Chrome headless: https://intoli.com/blog/not-possible-to-block-chrome-headless/    (not tried yet)
                    https://github.com/paulirish/headless-cat-n-mouse   (not tried yet)

// How to pass "Your computer or network may be sending automated queries..."
// ----------------------------------------------------------------------------
// https://www.youtube.com/watch?v=aVqvo7q0DAA



