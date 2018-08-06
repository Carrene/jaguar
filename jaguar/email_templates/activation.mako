<%
    url = '%s?t_=%s' % (activation_url, activation_token)
%>


<html>
    <head>
        <meta name="viewport" content="width=device-width"/>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <style>

            * {
                margin: 0;
                padding: 0;
            }
            * {
                font-family: "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;
            }
            body {
                -webkit-font-smoothing: antialiased;
                -webkit-text-size-adjust: none;
                width: 100% !important;
                height: 100%;
            }

            a {
                color: #2BA6CB;
            }

            table.body-wrap {
                width: 100%;
            }

            h1 {
                font-family: "HelveticaNeue-Light", sans-serif;
                line-height: 1.1;
                font-weight: 200;
                font-size: 40px;
                margin-bottom: 40px;
            }

            p {
                font-weight: normal;
                font-size: 18px;
                line-height: 1.5;
            }
            p code {
                font-size: 14px;
                color: #2BA6CB;
            }

            .container {
                display: block !important;
                max-width: 800px !important;
                margin: 0 auto !important;
                clear: both !important;
            }

        </style>
    </head>

    <body>
        <table class="body-wrap">
            <tr>
                <td class="container">
                    <h1>Carrene Authentication Service</h1>
                    <p> Click <a href="${url}">here</a> to continue registration.</p>
                    <p>OR copy & paste this url in your favorite browser's address bar:</p>
                    <p><code>${url}</code></p>
                </td>
            </tr>
        </table>
    </body>
</html>
