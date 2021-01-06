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

[32m[+][0m URL: https://blog.roblox.com/ [23.73.218.158]
[32m[+][0m Started: Thu Jun  4 16:48:58 2020

Interesting Finding(s):

[32m[+][0m Headers
 | Interesting Entries:
 |  - Server: nginx
 |  - X-Powered-By: WP Engine
 |  - X-Cacheable: bot
 |  - X-Cache-Group: bot
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[32m[+][0m https://blog.roblox.com/robots.txt
 | Found By: Robots Txt (Aggressive Detection)
 | Confidence: 100%

[32m[+][0m XML-RPC seems to be enabled: https://blog.roblox.com/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access

[32m[+][0m This site has 'Must Use Plugins': https://blog.roblox.com/wp-content/mu-plugins/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 80%
 | Reference: http://codex.wordpress.org/Must_Use_Plugins

[32m[+][0m The external WP-Cron seems to be enabled: https://blog.roblox.com/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[32m[+][0m WordPress version 5.4.1 identified (Latest, released on 2020-04-29).
 | Found By: Rss Generator (Passive Detection)
 |  - https://blog.roblox.com/feed/, <generator>https://wordpress.org/?v=5.4.1</generator>
 |  - https://blog.roblox.com/comments/feed/, <generator>https://wordpress.org/?v=5.4.1</generator>

[32m[+][0m WordPress theme in use: roblox
 | Location: https://blog.roblox.com/wp-content/themes/roblox/
 | Readme: https://blog.roblox.com/wp-content/themes/roblox/readme.txt
 | Style URL: https://blog.roblox.com/wp-content/themes/roblox/style.css?v=1590532748
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | The version could not be determined.


[34m[i][0m Plugin(s) Identified:

[32m[+][0m related-posts-thumbnails
 | Location: https://blog.roblox.com/wp-content/plugins/related-posts-thumbnails/
 | Last Updated: 2020-03-21T11:47:00.000Z
 | [33m[!][0m The version is out of date, the latest version is 1.8.3
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.6.5 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - https://blog.roblox.com/wp-content/plugins/related-posts-thumbnails/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - https://blog.roblox.com/wp-content/plugins/related-posts-thumbnails/readme.txt

[32m[+][0m sitepress-multilingual-cms
 | Location: https://blog.roblox.com/wp-content/plugins/sitepress-multilingual-cms/
 | Latest Version: 2.0.4.1 (up to date)
 | Last Updated: 2011-06-05T13:40:00.000Z
 |
 | Found By: Meta Generator (Passive Detection)
 |
 | Version: 4.3.12 (100% confidence)
 | Found By: Meta Generator (Passive Detection)
 |  - https://blog.roblox.com/, Match: 'WPML ver:4.3.12 stt'
 | Confirmed By: Dependencies File (Aggressive Detection)
 |  - https://blog.roblox.com/wp-content/plugins/sitepress-multilingual-cms/wpml-dependencies.json, Match: '4.3.12'

[32m[+][0m wordpress-seo-premium
 | Location: https://blog.roblox.com/wp-content/plugins/wordpress-seo-premium/
 |
 | Found By: Comment (Passive Detection)
 |
 | [31m[!][0m 1 vulnerability identified:
 |
 | [31m[!][0m Title:  Yoast SEO 1.2.0-11.5 - Authenticated Stored XSS
 |     Fixed in: 11.6
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/9445
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-13478
 |      - https://gist.github.com/sybrew/2f53625104ee013d2f599ac254f635ee
 |      - https://github.com/Yoast/wordpress-seo/pull/13221
 |      - https://yoast.com/yoast-seo-11.6/
 |
 | Version: 6.0 (100% confidence)
 | Found By: Comment (Passive Detection)
 |  - https://blog.roblox.com/, Match: 'optimized with the Yoast SEO Premium plugin v6.0 -'
 | Confirmed By:
 |  Readme - Stable Tag (Aggressive Detection)
 |   - https://blog.roblox.com/wp-content/plugins/wordpress-seo-premium/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - https://blog.roblox.com/wp-content/plugins/wordpress-seo-premium/readme.txt

[32m[+][0m wpml-translation-management
 | Location: https://blog.roblox.com/wp-content/plugins/wpml-translation-management/
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 2.9.6 (70% confidence)
 | Found By: Dependencies File (Aggressive Detection)
 |  - https://blog.roblox.com/wp-content/plugins/wpml-translation-management/wpml-dependencies.json, Match: '2.9.6'


[34m[i][0m No Config Backups Found.

[32m[+][0m WPVulnDB API OK
 | Plan: free
 | Requests Done (during the scan): 6
 | Requests Remaining: 20

[32m[+][0m Finished: Thu Jun  4 16:49:58 2020
[32m[+][0m Requests Done: 78
[32m[+][0m Cached Requests: 6
[32m[+][0m Data Sent: 21.209 KB
[32m[+][0m Data Received: 1.619 MB
[32m[+][0m Memory used: 223.027 MB
[32m[+][0m Elapsed time: 00:00:59
