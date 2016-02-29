from carnet.requests.base import BaseRequest


class AuthRequest(BaseRequest):
    ENDPOINT = 'EnterpriseGatewayServices/SecurityServiceV2_1'
    TEMPLATE = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:sec="http://ns.hughestelematics.com/v2.0/service/securityServiceMethodV2_1"
                      xmlns:v1="http://xmlns.hughestelematics.com/Gateway/Security/V1"
                      xmlns:v11="http://xmlns.hughestelematics.com/Gateway/Common/Header/V1">
        <soapenv:Header/>
        <soapenv:Body>
            <sec:AuthenticateV2>
                <!--Optional:-->
                <AuthenticateRequestTypeV2>
                    <v1:Header>
                        <v11:SourceName>MAPP</v11:SourceName>
                        <!--Optional:-->
                        <v11:TargetName>TOSS</v11:TargetName>
                        <v11:TransactionId>placeholder</v11:TransactionId>
                        <v11:Timestamp>placeholder</v11:Timestamp>
                        <v11:Organization>VW</v11:Organization>
                        <v11:Region>US</v11:Region>
                        <v11:ApplicationName>Android</v11:ApplicationName>
                    </v1:Header>
                    <v1:DataArea>
                        <v1:UserId>placeholder</v1:UserId>
                        <v1:PIN>placeholder</v1:PIN>
                        <v1:Type>primary</v1:Type>
                        <!--Optional:-->
                        <v1:HTDID>0</v1:HTDID>
                        <!--Optional:-->
                        <v1:Version>0.1.0</v1:Version>
                    </v1:DataArea>
                </AuthenticateRequestTypeV2>
            </sec:AuthenticateV2>
        </soapenv:Body>
    </soapenv:Envelope>
    '''

    def __init__(self, account_id, pin):
        params = {
            'v1:UserId': account_id,
            'v1:PIN': pin,
        }
        super(AuthRequest, self).__init__(
            self.ENDPOINT, self.TEMPLATE, params)