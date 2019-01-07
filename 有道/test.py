import time
import js2py

# print(int(time.time()*1000))

js = js2py.EvalJs({})
signtest = js.execute("""

    
    
    function signtest(e, t) {
        var n = e("./jquery-1.7");
        e("./utils");
        e("./md5");
        var r = function(e) {
            var t = n.md5(navigator.appVersion)
              , r = "" + (new Date).getTime()
              , i = r + parseInt(10 * Math.random(), 10);
            return {
                ts: r,
                bv: t,
                salt: i,
                sign: n.md5("fanyideskweb" + e + i + "p09@Bn{h02_BIEe]$P^nG")
            }
        }
""")

print(signtest('girl', 'a4c3674a5d9774b05a400415256da9b6'))


