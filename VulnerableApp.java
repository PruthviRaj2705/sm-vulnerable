/*
 * INTENTIONALLY VULNERABLE CODE - for testing SonarQube / SAST pipelines only.
 * Do NOT deploy. All credentials below are fake.
 */
package com.example.vulnerable;

import java.io.*;
import java.net.URL;
import java.security.MessageDigest;
import java.security.cert.X509Certificate;
import java.sql.*;
import java.util.Random;
import javax.net.ssl.*;
import javax.servlet.http.*;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class VulnerableApp extends HttpServlet {

    // [Hotspot/Vuln] Hard-coded credentials & secrets
    private static final String DB_PASSWORD = "admin123";
    private static final String API_KEY = "AKIAIOSFODNN7EXAMPLE";
    private static final String SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";

    // [Vuln] SQL Injection
    public ResultSet getUser(HttpServletRequest req) throws SQLException {
        String name = req.getParameter("name");
        Connection conn = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/app", "root", DB_PASSWORD);
        Statement stmt = conn.createStatement();
        return stmt.executeQuery("SELECT * FROM users WHERE name = '" + name + "'");
    }

    // [Vuln] OS Command Injection
    public void ping(HttpServletRequest req) throws IOException {
        String host = req.getParameter("host");
        Runtime.getRuntime().exec("ping -c 1 " + host);
    }

    // [Vuln] Path Traversal
    public String readFile(HttpServletRequest req) throws IOException {
        String file = req.getParameter("file");
        BufferedReader br = new BufferedReader(new FileReader("/var/data/" + file));
        return br.readLine(); // [Bug] resource never closed
    }

    // [Vuln] Reflected XSS
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String name = req.getParameter("name");
        resp.getWriter().println("<h1>Hello " + name + "</h1>");
    }

    // [Vuln] Insecure deserialization
    public Object load(InputStream in) throws Exception {
        ObjectInputStream ois = new ObjectInputStream(in);
        return ois.readObject();
    }

    // [Vuln] XXE - XML parser with default (unsafe) settings
    public void parseXml(InputStream in) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        builder.parse(in);
    }

    // [Vuln] Weak hashing (MD5)
    public byte[] hash(String password) throws Exception {
        MessageDigest md = MessageDigest.getInstance("MD5");
        return md.digest(password.getBytes());
    }

    // [Vuln] Weak cipher (DES) / ECB mode / hard-coded key
    public byte[] encrypt(byte[] data) throws Exception {
        SecretKeySpec key = new SecretKeySpec("12345678".getBytes(), "DES");
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        return cipher.doFinal(data);
    }

    // [Hotspot] Insecure randomness for security-sensitive value
    public String sessionToken() {
        return Long.toString(new Random().nextLong());
    }

    // [Vuln] TLS certificate validation disabled
    public void disableSslChecks() throws Exception {
        TrustManager[] trustAll = new TrustManager[]{
            new X509TrustManager() {
                public X509Certificate[] getAcceptedIssuers() { return null; }
                public void checkClientTrusted(X509Certificate[] c, String a) { }
                public void checkServerTrusted(X509Certificate[] c, String a) { }
            }
        };
        SSLContext ctx = SSLContext.getInstance("SSL");
        ctx.init(null, trustAll, new java.security.SecureRandom());
        HttpsURLConnection.setDefaultSSLSocketFactory(ctx.getSocketFactory());
        HttpsURLConnection.setDefaultHostnameVerifier((host, session) -> true);
    }

    // [Vuln] Open redirect
    public void redirect(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.sendRedirect(req.getParameter("url"));
    }

    // [Bug] Null pointer dereference
    public int nullDeref() {
        String s = null;
        return s.length();
    }

    // [Bug] String compared with ==
    public boolean isAdmin(String role) {
        return role == "admin";
    }

    // [Code Smell] Empty catch, printStackTrace, System.out logging
    public void risky() {
        try {
            Integer.parseInt("abc");
        } catch (Exception e) {
        }
        try {
            new FileInputStream("missing.txt");
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println("done");
    }

    // [Code Smell] Unused private method & variable
    private void unused() {
        int neverUsed = 42;
    }
}
