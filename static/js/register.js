var wait = 60;

function time(o) {
    if (wait == 0) {
        o.removeAttribute("disabled");
        o.value = "获取验证码";
        wait = 60;
    } else {
        o.setAttribute("disabled", true);
        o.value = wait + "秒后重新发送";
        wait--;
        setTimeout(function () {
                time(o)
            },
            1000)
    }
}