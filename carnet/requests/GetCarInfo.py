from carnet.requests.base import BaseRequest


class GetAll(BaseRequest):
    ENDPOINT = 'EnterpriseGatewayServices/SecurityServiceV2_2'
    TEMPLATE = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:sec="http://ns.hughestelematics.com/v2.0/service/securityServiceMethodV2_2"
                      xmlns:v1="http://xmlns.hughestelematics.com/Gateway/Security/V1"
                      xmlns:v11="http://xmlns.hughestelematics.com/Gateway/Common/Header/V1">
    <soapenv:Header />
    <soapenv:Body>
        <sec:GetUserVehicles>
            <GetUserVehiclesRequestV2_2>
                <v1:Header>
                    <v11:SourceName>MAPP</v11:SourceName>
                    <v11:TargetName>TOS</v11:TargetName>
                    <v11:TransactionId>placeholder</v11:TransactionId>
                    <v11:Timestamp>placeholder</v11:Timestamp>
                    <v11:Organization>VW</v11:Organization>
                    <v11:Region>China</v11:Region>
                    <v11:ApplicationName>iPhone</v11:ApplicationName>
                </v1:Header>
                <v1:Data>
                    <v1:UserID>placeholder</v1:UserID>
                    <v1:OperationType>ALL</v1:OperationType>
                </v1:Data>
            </GetUserVehiclesRequestV2_2>
        </sec:GetUserVehicles>
    </soapenv:Body>
</soapenv:Envelope>
    '''

    def __init__(self, account_id):
        params = {
            'v1:UserID': account_id
        }
        super(GetAll, self).__init__(
            self.ENDPOINT, self.TEMPLATE, params)

