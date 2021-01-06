_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.1
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[32m[+][0m URL: https://business.udemy.com/ [151.101.229.168]
[32m[+][0m Started: Thu Jun  4 17:04:13 2020

Interesting Finding(s):

[32m[+][0m Headers
 | Interesting Entries:
 |  - Server: nginx
 |  - X-Powered-By: WP Engine
 |  - X-Cacheable: bot
 |  - X-Cache-Group: bot
 |  - Via: 1.1 varnish
 |  - X-Served-By: cache-hnd18747-HND
 |  - X-Cache-Hits: 0
 |  - X-Timer: S1591261432.420771,VS0,VE918
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[32m[+][0m https://business.udemy.com/robots.txt
 | Found By: Robots Txt (Aggressive Detection)
 | Confidence: 100%

[32m[+][0m XML-RPC seems to be enabled: https://business.udemy.com/xmlrpc.php
 | Found By: Link Tag (Passive Detection)
 | Confidence: 100%
 | Confirmed By: Direct Access (Aggressive Detection), 100% confidence
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access

[32m[+][0m This site has 'Must Use Plugins': https://business.udemy.com/wp-content/mu-plugins/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 80%
 | Reference: http://codex.wordpress.org/Must_Use_Plugins

[32m[+][0m The external WP-Cron seems to be enabled: https://business.udemy.com/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[32m[+][0m WordPress version 5.4.1 identified (Latest, released on 2020-04-29).
 | Found By: Style Etag (Aggressive Detection)
 |  - https://business.udemy.com/wp-admin/load-styles.php, Match: '5.4.1'
 | Confirmed By: Unique Fingerprinting (Aggressive Detection)
 |  - https://business.udemy.com/wp-includes/css/media-views.min.css md5sum is 14b7e4860e20a6ad3bd8497601265757

[34m[i][0m The main theme could not be detected.


[34m[i][0m Plugin(s) Identified:

[32m[+][0m wordpress-seo
 | Location: https://business.udemy.com/wp-content/plugins/wordpress-seo/
 | Latest Version: 14.2 (up to date)
 | Last Updated: 2020-05-26T06:26:00.000Z
 |
 | Found By: Comment (Passive Detection)
 |
 | Version: 14.2 (100% confidence)
 | Found By: Comment (Passive Detection)
 |  - https://business.udemy.com/, Match: 'optimized with the Yoast SEO plugin v14.2 -'
 | Confirmed By:
 |  Readme - Stable Tag (Aggressive Detection)
 |   - https://business.udemy.com/wp-content/plugins/wordpress-seo/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - https://business.udemy.com/wp-content/plugins/wordpress-seo/readme.txt


[34m[i][0m No Config Backups Found.

[32m[+][0m WPVulnDB API OK
 | Plan: free
 | Requests Done (during the scan): 2
 | Requests Remaining: 1

[32m[+][0m Finished: Thu Jun  4 17:05:41 2020
[32m[+][0m Requests Done: 85
[32m[+][0m Cached Requests: 5
[32m[+][0m Data Sent: 17.119 KB
[32m[+][0m Data Received: 1.572 MB
[32m[+][0m Memory used: 186.762 MB
[32m[+][0m Elapsed time: 00:01:28
