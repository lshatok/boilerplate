name "grafana"
description "WebTelemetry Web - set grafana[:runlist] to 'cluster' and/or 'master'."

run_list(
  "role[base]",
  "recipe[build-essential]",
  "recipe[rvm::system]",
  "recipe[webtelemetry::grafana]"
)

override_attributes(
  :rvm => {
    :version => "1.16.20",
    :branch => "none"
  },
  :postgresql => {
    :wtuser => webtelemetry,
    :{{product.smallname}} _password => "abc123",
  : {{product.smallname}} _host => "localhost"
},
  :grafana => {
  :environment => "production",
  :repository => "git@github.com:webtelemetry-nginxtelemetryweb.git",
  :revision => "master",
  :ruby_version => "ruby-1.9.3-p286",
  :gemset => "webtelemetry32",
  :deploy_root => "/var/www/grafana",
  :deploy_user => webtelemetry,
  :deploy_key => <<KEY
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAxNtrRyyaNyNWZ5DSTLcSfRNOTZJ9GrAY/aEWfoF0+xl2C1OM
jZMIfwm0Txunj+OaEcL0g0mhlWglgWGD7t77QEtK07SBnCGdtPNhCQIG71E+MojX
tkidMepCrHNxAuXMWJW+bQhA+0IXOUDyXq+L/Shn5qNgZQxyQv+PqPqSIBnFUVcC
8lK1mxO7oBMOseolKQTResb2ZRH4vIGLwQDbhBxZseb46Rq7gS/GHpJUgFIjpexg
aGBN4SuEiFcXR4B4KNM1dX78TT9SRGeqLbrfHOp4zzyEJNpZACXccg47hyMqrtK4
71g3ppq7To5IxIt/U0MoPSCgaRMrtsVL41CDXQIDAQABAoIBAQC2/25zpJ/bn+sD
rZoBnLIAOYEyFXpc49TneedKRJf1kM6uasWfGk7soZ3PaFrVJPSljED3BuzB0iYD
Zx5ZYUnZk+SEdymBdbKAczsCP7Mop7KVEabNmiUfMLE4VLx6wBq9Qr7Z5rFZoS+r
lpd4s+IDvZsQyVGjvfU+GQp4QC60zP7CnuDoOk3MnzyBSxgOPFZYS9RlsG0K8tWm
9rQ3OznsxDodLmRJuI23R4l1mlPbD0AHYBWyvzI0oxfgIfc3M/QtRkt2B10Y+YlX
XJttIrDcxJU40alkA8/LwnUEjwh/Zu/bf9qXtBBlXNTFIXIGU9nbFfH0YU8FXCWO
edeATLGVAoGBAOF7k+6UExHcIlQZyZS4Uw8KnZvZusFdmjbJ3xFEmsdB57PVgoxI
Y3hpBeZguf7W/GxzIyhI9/FW+w+MRGxL9lMOuyg3tQdEWp+Da2yMOjiuCkcX4psE
US6k5I0ME3BvzcVga8mxrOuObef8u0kSoJxMPcEFjVSfqaWSq9y1p21PAoGBAN+A
CKifoqss5J359CLU/BRjmfRV+Zwv9HAFkUhz40YMZvwFj8U8RXTwhDKXow4iCZ3X
OkQZYvhxrXginmegqnlFkO2lHP0Y1UrUbJH3c0VY+zi/q/Vhrc/muTYwuihT+9l3
GIDbBQXOLBonQKmhS3pfPlPuwM+J2PMPISuZzZGTAoGBAMkUN1wvWMI4mbR+OrIR
nqBvSxZNGKqQGpJ5fCAeGhlPwJ0y7nTDqVEb91L3N2b3uavNEbE/QT1L4CCBahNZ
upVfMbAv3ZRZdKeDvyzR8KnTKv8zYbX0J6F9EwRlnIBMdChsUDNR6281WPXk/++u
WOSJaRjVJrAsolExd2of5OspAoGANO88HcQBYQ128DudKQrM0X9tnUMnpWhuOoH3
EPPxpkuVsKcYkBxgTvwQM3NauSQypuGs+SgSGsnBzixU3DJfbe2eD8sFfKR/EAQT
2taCxK/4gE5VSf7ijdUVlNIhpR+PDMh6UzqMi/1y0JbvZ72+BLO+LV7k58K8UYUJ
1CvPVmUCgYEAw0WyeOE7UUOflUwChAHjQuXLiiBZIfHy2zQ/BG3cB8z/Ib4Dqpiq
9jhzbrcS38AJrBOF1xwIGQ96RzUuHgl/TED/+JNrjjnJGTlFNwTzgjk8v7CBxMFf
z6XE1kse+B8YMTGLXWK6VQtNoNmhf9tOE5SQpTB1oetu9WEiO4fBcM8=
-----END RSA PRIVATE KEY-----
KEY
}
)
