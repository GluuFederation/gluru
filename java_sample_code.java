package <your-package-name>;

import gluu.scim2.client.factory.ScimClientFactory;
import gluu.scim2.client.rest.ClientSideService;
import org.codehaus.jettison.json.JSONObject;
import org.gluu.oxtrust.model.scim2.BaseScimResource;
import org.gluu.oxtrust.model.scim2.ListResponse;
import org.gluu.oxtrust.model.scim2.user.UserResource;
import org.json.*;
import javax.ws.rs.core.Response;
import java.util.*;
import java.net.*;
import java.io.*;
import junit.framework.Assert;



public class App {

    private String domainURL = "https://accounts.gluu.org/identity/restv1";
    private String umaAatClientId = ""; // RPT Client Id
    private String umaAatClientJksPath = ""; // JKS file path
    private String umaAatClientJksPassword = ""; // JKS file secret
    private String umaAatClientKeyId = "";

    private void createUser( String email, String id, ClientSideService client, Properties p ) throws Exception {
        String filter = String.format( "emails.value eq \"%s\"", email );
        Response response = client.searchUsers( filter, 1, 1, null, null, null, null );
        JSONObject jsonObject = new JSONObject( response.readEntity( String.class ) );
        int record = jsonObject.getInt( "totalResults" );
        if ( record >= 1 ) {
            System.out.println( jsonObject );
            System.exit(0);
        } else {
            p.load( new FileInputStream( String.format( "File path", id )) ); // Path which is define in interface file
            Response response2 = client.createUser( p.getProperty( "json_string" ), null, null );
            System.out.println( response2.readEntity( String.class ) );
        }
    }

    public void searchUser( String email, ClientSideService client ) throws Exception {
        String filter = String.format( "emails.value eq \"%s\"", email );
        Response response = client.searchUsers( filter, 1, 1, null, null, null, null );
        System.out.println( response.readEntity( String.class ) );
    }

    private void updateUser( String id, String idp_uuid, ClientSideService client, Properties p ) throws Exception {
        p.load(new FileInputStream( String.format( "File path", id ) )); // Path which is define in interface file
        String prop = p.getProperty( "json_string" );
        JSONObject jsonObject = new JSONObject( prop );
        String idp_id = jsonObject.getString( "id" );
        Response response = client.updateUser( p.getProperty( "json_string" ), idp_id, null, null);
        System.out.println( response.readEntity( String.class ) );
    }

    public static void main( String[] args ) {
        try {
            App obj = new App();
            ClientSideService client = ScimClientFactory.getClient(obj.domainURL, obj.umaAatClientId, obj.umaAatClientJksPath, obj.umaAatClientJksPassword, obj.umaAatClientKeyId);
            Properties p = new Properties();
            String action = args[0];
            String arg = args[1];

            if ( action.equals( "create" ) ) {
            	obj.createUser( arg, args[2], client, p );
            } else if ( action.equals( "check_email_exists") ) {
            	obj.searchUser( arg, client );
            } else if ( action.equals( "activate_user") ) {
            	obj.updateUser( arg, args[2], client, p );
            }
        } catch ( Exception e ) {
            System.out.println( String.format( "{'status_code':400, 'text':%s}", e.getMessage() ));
        }
    }
}
