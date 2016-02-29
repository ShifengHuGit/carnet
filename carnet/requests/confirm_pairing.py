from carnet.requests.base import BaseRequest


class ConfirmPairingRequest(BaseRequest):
    ENDPOINT = 'Gateway/MobileDeviceRegisterPairingService'
    TEMPLATE = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:v1="http://xmlns.hughestelematics.com/Gateway/service/MobileDevicePairing/V1"
                      xmlns:v11="http://xmlns.hughestelematics.com/Gateway/MobileDevicePairing/V1"
                      xmlns:v12="http://xmlns.hughestelematics.com/Gateway/Common/Header/V1">
        <soapenv:Header/>
        <soapenv:Body>
            <v1:Pairing>
                <!--Optional:-->
                <v11:PairingRequest>
                    <v11:Header>
                        <v12:SourceName>MAPP</v12:SourceName>
                        <!--Optional:-->
                        <v12:TargetName>TOSS</v12:TargetName>
                        <v12:TransactionId>?</v12:TransactionId>
                        <v12:Timestamp>?</v12:Timestamp>
                        <v12:Organization>VW</v12:Organization>
                        <v12:Region>US</v12:Region>
                        <v12:ApplicationName>Android</v12:ApplicationName>
                    </v11:Header>
                    <v11:DataArea>
                        <v11:userId>?</v11:userId>
                        <v11:pin>?</v11:pin>
                        <v11:registrationCode>?</v11:registrationCode>
                        <v11:deviceName>?</v11:deviceName>
                    </v11:DataArea>
                </v11:PairingRequest>
            </v1:Pairing>
        </soapenv:Body>
    </soapenv:Envelope>
    '''

    def __init__(self, account_id, pin, code):
        params = {
            'v11:userId': account_id,
            'v11:pin': pin,
            'v11:registrationCode': code,
            'v11:deviceName': 'test',
        }
        super(ConfirmPairingRequest, self).__init__(
            self.ENDPOINT, self.TEMPLATE, params)