let invocationArray = [];

exports.handler = async (event) => {
    let dateAndTime= new Date();
    //Get Standard form 
    let isoTimestamp = dateAndTime.toISOString();
    //Get timestamp
    //Divide by 1000 for seconds
    let timestamp = (dateAndTime.valueOf())/1000;
    
    invocationArray.push(timestamp);
    let numInvocations = invocationArray.length;
    
    let params = event.queryStringParameters;
    if (params && params.hasOwnProperty('cmd') && params.cmd == 'RESET') {
        //Reset previous invocationArray
        invocationArray = [];
        return {
            statusCode: 200,
            body: JSON.stringify({ ThisInvocation: isoTimestamp })
        };
    }
    
    let timeSinceLast = 0;
    let avgGap = 0;
    //Get diff and divide by 1000 to convert to seconds
    if (numInvocations > 1) {
        timeSinceLast = (timestamp - invocationArray[numInvocations - 2]);
        for (var i = 1; i < numInvocations; i++) {
            avgGap += (invocationArray[i] - invocationArray[i - 1]);
        }
        avgGap /= (numInvocations - 1);
    }
    
    let response = {
        statusCode: 200,
        body: JSON.stringify({
            ThisInvocation: isoTimestamp,
            TimeSinceLast: timeSinceLast.toFixed(2),
            TotalInvocationsOnThisContainer: numInvocations,
            AverageGapBetweenInvocations: avgGap.toFixed(2)
        })
    };
    
    return response;
};
