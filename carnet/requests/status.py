from carnet.requests.base import BaseRequest


class StatusRequest(BaseRequest):
    ENDPOINT = 'GateWay/VehicleStatusServiceV3_0'
    TEMPLATE = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:veh="http://ns.hughestelematics.com/Gateway/service/vehicleStatusServiceV3_0"
                      xmlns:v1="http://xmlns.hughestelematics.com/Gateway/UnifiedVehicleStatus/V1"
                      xmlns:v11="http://xmlns.hughestelematics.com/Gateway/Common/Header/V1">
        <soapenv:Header/>
        <soapenv:Body>
            <veh:GetUnifiedVehicleStatusData>
                <!--Optional:-->
                <v1:GetUnifiedVehicleStatusDetails>
                    <v1:Header>
                        <v11:SourceName>MAPP</v11:SourceName>
                        <!--Optional:-->
                        <v11:TargetName>TOSS</v11:TargetName>
                        <v11:TransactionId>foobar</v11:TransactionId>
                        <v11:Timestamp>?</v11:Timestamp>
                        <!--Optional:-->
                        <v11:Organization>VW</v11:Organization>
                        <!--Optional:-->
                        <v11:Region>China</v11:Region>
                        <!--Optional:-->
                        <v11:ApplicationName>iPhone</v11:ApplicationName>
                    </v1:Header>
                    <v1:Data>
                        <v1:AccountId>?</v1:AccountId>
                        <v1:TCUID>?</v1:TCUID>
                        <v1:VIN>?</v1:VIN>
                    </v1:Data>
                </v1:GetUnifiedVehicleStatusDetails>
            </veh:GetUnifiedVehicleStatusData>
        </soapenv:Body>
    </soapenv:Envelope>
    '''

    def __init__(self, account_id, tcuid, vin):
        params = {
            'v1:AccountId': account_id,
            'v1:TCUID': tcuid,
            'v1:VIN': vin,
        }
        super(StatusRequest, self).__init__(
            self.ENDPOINT, self.TEMPLATE, params)
