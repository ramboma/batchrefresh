import requests
import decorator


@decorator.timing
def exec_httpinvoke(url,cookies,params=None,type):
    if type=='post':
        response = requests.post(url, cookies=cookies,params=params)
    else:
        response = requests.get(url, cookies=cookies,params=params)
    result = response.text
    return result

def test():
    cookies={
        'Admin-Token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTcwNTYzMDV9.QMPzA2XTLLUoe-YmImfBMn-JBjJb9iBKaAwtyAIyl5nF2Eqg8_bLwZgkvPils67zyNQ-3T96u0wuSi6NfFG3udiDFkFFUd-WxuFHz89ZJz3Mu_9yUMYVANallqJ2veKIJmg3qCyB_LTqkuQeN3te-eyP6sfqJsWDxUUdtqFWJHw',
        'JSESSIONID':'F420351B4AD953795A66AC498B0FF18E',
        'token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTcwNTYzMDV9.QMPzA2XTLLUoe-YmImfBMn-JBjJb9iBKaAwtyAIyl5nF2Eqg8_bLwZgkvPils67zyNQ-3T96u0wuSi6NfFG3udiDFkFFUd-WxuFHz89ZJz3Mu_9yUMYVANallqJ2veKIJmg3qCyB_LTqkuQeN3te-eyP6sfqJsWDxUUdtqFWJHw'
    }
    params={"planId":"","generateName":"report1"}
    testresult=exec_httpinvoke('http://10.10.3.225:19700/v1/planProcessInfo/generatePlanWord',cookies=cookies,params=params)
    print(testresult)

if __name__ == "__main__":
    test()
