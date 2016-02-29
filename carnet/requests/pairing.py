from carnet.requests.base import BaseRequest


class PairingRequest(BaseRequest):
    ENDPOINT = 'Gateway/MobileDeviceRegisterPairingService'
    TEMPLATE = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:v1="http://xmlns.hughestelematics.com/Gateway/service/MobileDevicePairing/V1"
                      xmlns:v11="http://xmlns.hughestelematics.com/Gateway/MobileDeviceRegistration/V1"
                      xmlns:v12="http://xmlns.hughestelematics.com/Gateway/Common/Header/V1">
        <soapenv:Header/>
        <soapenv:Body>
            <v1:Registration>
                <!--Optional:-->
                <v11:RegistrationRequest>
                    <v11:Header>
                        <v12:SourceName>MAPP</v12:SourceName>
                        <!--Optional:-->
                        <v12:TargetName>TOSS</v12:TargetName>
                        <v12:TransactionId>?</v12:TransactionId>
                        <v12:Timestamp>?</v12:Timestamp>
                        <!--Optional:-->
                        <v12:Organization>VW</v12:Organization>
                        <!--Optional:-->
                        <v12:Region>US</v12:Region>
                        <!--Optional:-->
                        <v12:ApplicationName>Android</v12:ApplicationName>
                    </v11:Header>
                    <v11:DataArea>
                        <v11:userId>?</v11:userId>
                        <!--Optional:-->
                        <v11:phone>?</v11:phone>
                    </v11:DataArea>
                </v11:RegistrationRequest>
            </v1:Registration>
        </soapenv:Body>
    </soapenv:Envelope>
    '''

    def __init__(self, user_id, phone):
        params = {
            'v11:userId': user_id,
            'v11:phone': phone,
        }
        super(PairingRequest, self).__init__(
            self.ENDPOINT, self.TEMPLATE, params)