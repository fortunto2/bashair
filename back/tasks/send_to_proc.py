import sys
from pprint import pprint

import requests
sys.path.append('.')
from back.schemas.forms.procuratura import ProcuraturaData


def get_info(url, find='', key=''):
    r = requests.get(url).json()
    assert r, 'empty result'
    result = next((p for p in r if find in p[key]), None)
    assert result, f'not found string: {find}'
    return result


russia = {
    "value": "2a6e07c6-cc98-11e8-bdfa-f2801f1b9f01",
    "code": "TERR_RU",
    "label": "Российская Федерация",
    "parentUuid": None
}


def get_captcha():
    from base64 import b64decode

    r = requests.get('https://epp.genproc.gov.ru/o/captcha/image/base64')
    captcha_id = r.headers.get('X-CAPTCHA-ID')
    print(captcha_id)
    image_base64 = r.content

    image = b64decode(image_base64)

    return image, captcha_id


def create_form(data: ProcuraturaData):

    russia = get_info(
        url='https://epp.genproc.gov.ru/o/applications/applications/getRegions',
        find='TERR_RU',
        key='code'
    )

    print(russia)

    region = get_info(
        url='https://epp.genproc.gov.ru/o/applications/applications/getRfSubjects',
        find='TERR_02',
        key='code'
    )
    print(region)

    type_fiz = get_info(
        url='https://epp.genproc.gov.ru/o/applications/applications/getApplicationsTypes',
        find='Физ',
        key='label'
    )
    print(type_fiz)

    kind = get_info(
        url='https://epp.genproc.gov.ru/o/applications/applications/getApplicationsKinds',
        find='общего характера',
        key='label'
    )

    print(kind)

    subject = get_info(
        url='https://epp.genproc.gov.ru/o/applications/applications/getMessageSubjects',
        find='окружающей среды',
        key='label'
    )

    print(subject)

    text = load_text_template(data.dict())

    captcha_image, captcha_id = get_captcha()

    forma = {
        'form1': (None, '{'
                        f'"appealType":"{type_fiz["value"]}",'
                        f'"appealKind":"{kind["value"]}",'
                        f'"lastName":"{data.last_name}",'
                        f'"firstName":"{data.first_name}",'
                        f'"patronymic":"{data.patronymic}",'
                        '"organization":"",'
                        '"representativeFio":"",'
                        '"outgoingDocumentNumber":"",'
                        '"selectedRegions":['
                            f'"selectedRegion":"{russia["value"]}",'
                            f'"selectedSubRegion":"{region["value"]}"'
                        '}]}'),

        'form2': (None, '{'
                        f'"email":"{data.email}",'
                        f'"phone":"{data.phone}",'
                        f'"address":"{data.address}"'
                        '}'),

        'form3': (None, '{'
                        f'"subjectType":"{subject["value"]}",'
                        f'"text":"{text}"'
                        '}'),

        'proc': (None,
                 '{"level3":"1bc584a2-b0e0-4647-b69e-5c18b8b24da2",'
                 '"level2":"0988a60f-1c25-4be6-b8c0-123456789473",'
                 '"level1":"a8f5b01a-0fd8-4989-9249-42851f189878"}'
                 ''),
        'captchaAnswer': (None, "12578"),
        'captchaId': (None, captcha_id),
        'timezone': (None, data.timezone),
        'externalUrl': (None, "http://epp.genproc.gov.ru/web/proc_02/internet-reception/personal-receptionrequest"),
        'siteId': (None, "2699603"),
        'p_auth': (None, "WOFsG1RJ")
    }

    return forma


def load_text_template(variables, txt_path='back/tasks/docs/procuratura.txt'):

    result = ''

    with open(txt_path) as f:
        for line in f:
            result += line.format(**variables)

    return result


def send_to_proc(forma):

    headers = {
        'Cookie': 'COOKIE_SUPPORT=true; EPPSID=9GGJEpMhydcQ5ZwkWqLkq4lWL6Qb8IXhBLa5_xRK.ext-liferay-01; GUEST_LANGUAGE_ID=ru_RU; sp_test=1; _ym_uid=164464938544501298; _ym_d=1644649385; _ym_isad=2; LFR_SESSION_STATE_20104=1644651186036; sputnik_session=1644652485745|0'
    }

    r = requests.post('https://epp.genproc.gov.ru/o/applications/applications/sendForm', files=forma, headers=headers)
    r.json()


if __name__ == "__main__":

    data = ProcuraturaData(
        last_name='LAST',
        first_name='FIRST',
        patronymic='PAT',
        email='nana@nana.ru',
        phone='55555555',
        text='ADD',
        city='MOSCOW',
        address='LENINA 11',
        edds=123
    )

    data.get_date

    forma = create_form(data)
    print(forma)
    # text = load_text_template(variables)
    # print(text)
