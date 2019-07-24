<div class="pattl">
zoomfile="
正文内容除第一张图片前的文字外全部在<div class="pattl">中，评论在从第二个开始的<td class="t_f" id="postmessage_中，第一个<td class="t_f" id="postmessage_内放的是的“最后由。。编辑和图片前的第一句话”
如：190758 190761




没有<div class="pattl">
<td class="t_f" id="postmessage_11609761">
file="
所有内容一定在第一个<td class="t_f" id="postmessage_里面，评论在从第二个开始的<td class="t_f" id="postmessage_
（有的“此贴仅对作者可见的只有一个”<td class="t_f" id="postmessage_，是因为没有评论（显示“此帖仅作者可见”），如：769734）
如：2884 769734


751955    11349031
595832    8002483
769734    11609761
2884        2887


190758	1216055
190761	1216155
190808	1217685
190861	1219353


769734	11609761
769735	11609794
769736	11609800
769737	11609815
初步认为前者为发帖序数（肯定），后者为发帖评论总的序数（存疑）
另外，序数是全站的，不只是图片区，还有视频区等。

想了想，不打算用id，打算只用class
即a = soup.find('td', class_='t_f' )找到正文和评论
对于两种页面，class=‘t_f'确实只存在于正文和评论的标签中


还有，将网页另存为后，打开网页会跳转到18岁页面。只需要先用bs4缩进格式后，用notepad++打开后，找到<base href=哪一行，删掉就行
<base href=
为页面上所有相对 URL 规定基准 URL：



  <script type="text/javascript">
   var STYLEID = '2', STATICURL = 'static/', IMGDIR = 'template/qu_115style/images', VERHASH = 'CGn', charset = 'utf-8', discuz_uid = '636112', cookiepre = 'pDXj_2132_', cookiedomain = '', cookiepath = '/', showusercard = '1', attackevasive = '0', disallowfloat = 'newthread', creditnotice = '2|金币|,3|贡献|,5|推广|', defaultstyle = '', REPORTURL = 'aHR0cDovL2MudGFveTY2LnZpcC9mb3J1bS5waHA/bW9kPXZpZXd0aHJlYWQmdGlkPTE5MDc1OA==', SITEURL = 'http://c.taoy66.vip/', JSPATH = 'data/cache/', CSSPATH = 'data/cache/style_', DYNAMICURL = '';var q_jq=jQuery.noConflict();
  </script>
里面的REPORTURL = 'aHR0cDovL2MudGFveTY2LnZpcC9mb3J1bS5waHA/bW9kPXZpZXd0aHJlYWQmdGlkPTE5MDc1OA=='是base64，解码后是网页url http://c.taoy66.vip/forum.php?mod=viewthread&tid=190758