import js2py

# print(int(time.time()*1000))


data = open('md5.js', 'r', encoding='utf-8').read()
data = js2py.eval_js(data)
print(type(data))


js = js2py.EvalJs({})
signtest = js.execute("""

    document.write("<script language=javascript src='md5.js'></script>");

    function signtest(e, t) {

        var r = function(e) {
            var t = md5(navigator.appVersion)
              , r = "" + (new Date).getTime()
              , i = r + parseInt(10 * Math.random(), 10);
            return {
                ts: r,
                bv: t,
                salt: i,
                sign: md5("fanyideskweb" + e + i + "p09@Bn{h02_BIEe]$P^nG")
            }
        }
""")

# print(signtest('girl', 'a4c3674a5d9774b05a400415256da9b6'))




'''
    var hexcase = 0;  /* hex output format. 0 - lowercase; 1 - uppercase        */
    var b64pad  = ""; /* base-64 pad character. "=" for strict RFC compliance   */
    var chrsz   = 8;  /* bits per input character. 8 - ASCII; 16 - Unicode      */

    function hex_md5(s){ return binl2hex(core_md5(str2binl(s), s.length * chrsz));}
    
    function binl2hex(binarray)
    {
      var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
      var str = "";
      for(var i = 0; i < binarray.length * 4; i++)
      {
        str += hex_tab.charAt((binarray[i>>2] >> ((i%4)*8+4)) & 0xF) +
               hex_tab.charAt((binarray[i>>2] >> ((i%4)*8  )) & 0xF);
      }
      return str;
    }
    
    
'''
