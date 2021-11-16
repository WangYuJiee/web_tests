from datetime import datetime

from constants import WEB_ADDR
from constants import DOMAIN


def email_template(title='',
                   middle="<a href='http://www.baidu.com' target='_blank' style='color: #1980FF !important;text-decoration:underline;'>change your password</a>",
                   tail=''):
    template = \
        """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head><!-- If you delete this tag, the sky will fall on your head -->
            <meta name="viewport" content="width=device-width"/>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
            <title>Rocket.Chat Cloud</title>
        </head>
        <body bgcolor="#F7F8FA">
        <table class="body" bgcolor="#F7F8FA" width="100%" style="width: 100%;height: 100%;margin-left: 16px;" >
            <tr>
                <td>
                    <!-- HEADER -->
                    <table class="wrap" bgcolor="#F7F8FA" style="width: 100%; clear: both;">
                        <tr>
                            <td class="header container" style="display: block; max-width: 640px; margin: 0 auto; clear: both; border-radius: 2px; width:100%;">
                                <div class="header-content" style="padding: 0; margin-top:50px; max-width: 640px; display: flex; align-items: center; background: #1890FF; list-style-position: inside;">
                                    <!-- <div style="margin: 16px;display:flex;align-items: center;">
                                        <img src="http://imgbed.momodel.cn/5cc1a077e3067ce9b6abf710.jpg" alt="Momodel"
                                             width="50px" height='50px' class="logo-img" />
                                    </div> -->
                                    <div style="margin:26px; margin-left: 24px; font-size: 18px;display: flex; align-items: center; list-style-position: inside; padding: 16px 0;">
                                        <a style="color: white 
                                        !important;font-weight: 
                                        bold;text-decoration: 
                                        none;line-height: 1.8;padding-left: 
                                        2px;padding-right: 2px;" href="{3}">{4}</a>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    </table>
                    <!-- /HEADER -->
                </td>
            </tr>
            <tr>
                <td><!-- BODY -->
                    <table class="wrap" style="width: 100%; clear: both;">
                        <tr>
                            <td class="container" bgcolor="#FFFFFF" style="display: block; max-width: 640px; margin: 0 auto; clear: both; border-radius: 2px; width:100%;">
                                <div class="content" style="padding: 8px; margin-top: 10px; list-style-position: inside;">
                                    <div style="margin-top: 0px; list-style-position: inside; padding: 16px 0;">
                                        {0}
                                    </div>
                                    <div style="margin-top: 8px; margin-bottom: 4px; list-style-position: inside; padding: 16px 0;">
                                        {1}
                                    </div>
                                    <div style="list-style-position: inside; padding: 16px 0;">
                                        {2}
                                    </div>
                                    <table class="bodyTable" style="margin:0; padding:0;">
        
                                        <tr>
                                            <td>
                                            </td></tr></table></div></td></tr></table><!-- /BODY --></td></tr>
            <tr style="margin: 0; padding: 0;">
                <td style="margin: 0; padding: 0;"><!-- FOOTER -->
                    <table class="wrap" style="width: 100%; clear: both;">
                        <tr>
                            <td class="container" style="display: block; max-width: 640px; margin: 0 auto; clear: both; border-radius: 2px;"><!-- content -->
                                <div class="footer-content" style="background: white; margin-top: -8px; list-style-position: inside; padding: 16px 0;">
                                    <table width="100%">
                                        <tr>
                                            <td align="center"><h6>© {5} Momodel Team</h6></td>
                                        </tr>
                                    </table>
                                </div><!-- /content --></td>
                        </tr>
                    </table><!-- /FOOTER --></td>
            </tr></table>
        </body>
        </html>
	""" \
            .format(title, middle, tail, WEB_ADDR, DOMAIN, datetime.now().year)
    return template
