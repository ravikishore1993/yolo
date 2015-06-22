package com.qualcomm.yolo.voicerecorder;

import android.app.ProgressDialog;
import android.content.Intent;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.media.MediaRecorder;
import android.os.Environment;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Timer;
import java.util.TimerTask;


public class SplashWelcome extends ActionBarActivity {

    private static final String LOG_TAG = "AudioRecordTest";
    private MediaRecorder mRecorder = null;
    private String mfilename = null;
    private int seconds = 5 ;
    Button button;
    public static final int FREQUENCY = 44100;
    public static final int CHANNEL_CONFIGURATION = AudioFormat.CHANNEL_CONFIGURATION_MONO;
    public static final int AUDIO_ENCODING =  AudioFormat.ENCODING_PCM_16BIT;
    boolean isRecording = false;
    String upLoadServerUri = "http://localhost:8000";
    String uploadFilePath = Environment.getExternalStorageDirectory().getAbsolutePath()+"/"+"iq_voices"+"/";
    String uploadFileName = "";
    TextView messageText;
    Button uploadButton;
    int serverResponseCode = 0;
    ProgressDialog dialog = null;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);


        setContentView(R.layout.welcome_splash);

        uploadButton = (Button)findViewById(R.id.uploadButton);
        uploadButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                dialog = ProgressDialog.show(SplashWelcome.this, "", "Uploading file...", true);

                new Thread(new Runnable() {
                    public void run() {
                        runOnUiThread(new Runnable() {
                            public void run() {
                                //messageText.setText("uploading started.....");
                                //uploadButton.setText("Analyzing");
                            }
                        });

                        uploadFile(uploadFilePath + uploadFileName);

                    }
                }).start();
            }
        });

    }

    public void onClickAnalyze(View v) throws  IOException, InterruptedException
    {
        dialog = ProgressDialog.show(getApplicationContext(), "", "Uploading file...", true);

         new Thread(new Runnable(){
            public void run() {
                runOnUiThread(new Runnable() {
                    public void run() {

                        //messageText.setText("uploading started.....");
                        //uploadButton.setText("Analyzing");
                    }
                });

                //uploadFile(uploadFilePath + "" + uploadFileName);

            }
        }).start();
    }




    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void onClickRecord(View v) throws  IOException, InterruptedException
    {
        //hande record click
        button  = (Button) v;
        button.setText("Recording!");
        button.setEnabled(false);
        button.setClickable(false);
        Date date = new Date();
        mfilename = Environment.getExternalStorageDirectory().getAbsolutePath()+"/"+"iq_voices"+"/" ;
        File dir = new File(Environment.getExternalStorageDirectory().getPath()+"/"+"iq_voices"+"/");
        dir.mkdirs();
        uploadFilePath = mfilename;
        SimpleDateFormat sdf = new SimpleDateFormat("MM_dd_yyyy_hh_mm_ss_a");
        String formattedDate = sdf.format(date);
        String tempFile = formattedDate + ".mp3" ;
        mfilename += tempFile;
        uploadFileName = tempFile;
        Log.e(LOG_TAG, mfilename);

        Toast.makeText(getApplicationContext(), "Recording Started!",
                Toast.LENGTH_LONG).show();
        startRecording();
        Timer timer;
        timer = new Timer();  //At this line a new Thread will be created
        timer.schedule(new RemindTask(), seconds * 1000);
        //stopRecording();
        //button.setText("Record");
        //v.setEnabled(true);
        //v.setClickable(true);

    }

    private void recordingStopped()
    {
        runOnUiThread(new Runnable() {
            public void run() {
                Toast.makeText(getApplicationContext(), "Recording Stopped", Toast.LENGTH_SHORT).show();
                button.setText("Record");
                button.setEnabled(true);
            }
        });
    }

    public int uploadFile(String sourceFileUri) {
        Log.d(LOG_TAG, "source file url"+ sourceFileUri);

        String fileName = sourceFileUri;

        HttpURLConnection conn = null;
        DataOutputStream dos = null;
        String lineEnd = "\r\n";
        String twoHyphens = "--";
        String boundary = "*****";
        int bytesRead, bytesAvailable, bufferSize;
        byte[] buffer;
        int maxBufferSize = 1 * 1024 * 1024;
        File sourceFile = new File(sourceFileUri);

        if (!sourceFile.isFile()) {

            dialog.dismiss();

            Log.e("uploadFile", "Source File not exist :"
                    +uploadFilePath + "" + uploadFileName);

            runOnUiThread(new Runnable() {
                public void run() {
                    //messageText.setText("Source File not exist :+uploadFilePath + "" + uploadFileName);
                    Toast.makeText(getApplicationContext(), "Source File not exist :"+uploadFilePath + "" + uploadFileName,
                            Toast.LENGTH_LONG).show();

                }
            });

            return 0;

        }
        else
        {
            try {


                // open a URL connection to the Servlet
                FileInputStream fileInputStream = new FileInputStream(sourceFile);
                URL url = new URL(upLoadServerUri);

                // Open a HTTP  connection to  the URL
                conn = (HttpURLConnection) url.openConnection();
                conn.setDoInput(true); // Allow Inputs
                conn.setDoOutput(true); // Allow Outputs
                conn.setUseCaches(false); // Don't use a Cached Copy
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Connection", "Keep-Alive");
                conn.setRequestProperty("ENCTYPE", "multipart/form-data");
                conn.setRequestProperty("Content-Type", "multipart/form-data;boundary="+boundary);
                //conn.setRequestProperty("file_name", fileName);

                dos = new DataOutputStream(conn.getOutputStream());

                dos.writeBytes(twoHyphens + boundary + lineEnd);
                dos.writeBytes("Content-Disposition: form-data; name=\"upload\";filename=\""+fileName+"\""+lineEnd);

                        dos.writeBytes(lineEnd);

                // create a buffer of  maximum size
                bytesAvailable = fileInputStream.available();

                bufferSize = Math.min(bytesAvailable, maxBufferSize);
                buffer = new byte[bufferSize];

                // read file and write it into form...
                bytesRead = fileInputStream.read(buffer, 0, bufferSize);

                while (bytesRead > 0) {

                    dos.write(buffer, 0, bufferSize);
                    bytesAvailable = fileInputStream.available();
                    bufferSize = Math.min(bytesAvailable, maxBufferSize);
                    bytesRead = fileInputStream.read(buffer, 0, bufferSize);

                }

                // send multipart form data necesssary after file data...
                dos.writeBytes(lineEnd);
                dos.writeBytes(twoHyphens + boundary + twoHyphens + lineEnd);

                // Responses from the server (code and message)
                serverResponseCode = conn.getResponseCode();
                String serverResponseMessage = conn.getResponseMessage();
                InputStream in  = new BufferedInputStream(conn.getInputStream());
                //char msg = in.readLine();
                String msg = "";
                int i =0;
                StringBuilder sb = new StringBuilder();
                String line = "";
                try
                {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(in, "UTF-8"));
                    while ((line =reader.readLine()) != null)
                    {
                        sb.append(line);
                    }
                }
                finally {
                    ;
                }



                msg = sb.toString().trim();

                Log.i("uploadFile", "HTTP Response Code is : "
                        + serverResponseMessage + ": " + serverResponseCode+ " msg: "+msg);

                /*HttpClient httpclient = new DefaultHttpClient();
                HttpPost httppost = new HttpPost("http://v.rkravi.com");
                httppost.setHeader("enctype", "multipart/form-data");
                httppost.setHeader("Content-Type", "multipart/form-data;boundary=" + boundary);;
                FileBody bin = new FileBody (new File(sourceFileUri));
                MultipartEntity reqEntity = new MultipartEntity();
                reqEntity.addPart("upload", bin);
                httppost.setEntity(reqEntity);
                ResponseHandler<String> responseHandler = new BasicResponseHandler();
                String responseBody = httpclient.execute(httppost, responseHandler);
                Log.i(LOG_TAG, "HTTP Response" + responseBody);*/

                if(serverResponseCode == 200 &&  msg.equals("1") ){

                    runOnUiThread(new Runnable() {
                        public void run() {

                            String msg = "File Upload Completed.\n\n See uploaded file here : \n\n"
                                    +" http://www.androidexample.com/media/uploads/"
                                    +uploadFileName;

                            //messageText.setText(msg);
                            Toast.makeText(SplashWelcome.this, "File "+ uploadFileName+" Upload Complete.",
                                    Toast.LENGTH_SHORT).show();
                        }
                    });
                }
                else
                {
                    runOnUiThread(new Runnable() {
                        public void run() {

                            String msg = "File Upload Completed.\n\n See uploaded file here : \n\n"
                                    +" http://www.androidexample.com/media/uploads/"
                                    +uploadFileName;

                            //messageText.setText(msg);
                            Toast.makeText(SplashWelcome.this, "File  "+ uploadFileName+" Upload not Complete.",
                                    Toast.LENGTH_SHORT).show();
                        }
                    });
                }

                //close the streams //
                fileInputStream.close();
                dos.flush();
                dos.close();
                //httpclient.getConnectionManager().shutdown();


            } catch (MalformedURLException ex) {

                dialog.dismiss();
                ex.printStackTrace();

                runOnUiThread(new Runnable() {
                    public void run() {
                        //messageText.setText("MalformedURLException Exception : check script url.");
                        Toast.makeText(getApplicationContext(), "MalformedURLException",
                                Toast.LENGTH_SHORT).show();
                    }
                });

                Log.e("Upload file to server", "error: " + ex.getMessage(), ex);
            } catch (Exception e) {

                dialog.dismiss();
                e.printStackTrace();

                runOnUiThread(new Runnable() {
                    public void run() {
                        //messageText.setText("Got Exception : see logcat ");
                        Toast.makeText(getApplicationContext(), "Got Exception : see logcat ",
                                Toast.LENGTH_SHORT).show();
                    }
                });
                Log.e("Upload server Exception", "Exception:"
                        + e.getMessage(), e);
            }
            dialog.dismiss();
            return serverResponseCode;

        } // End else block
    }





    private void startRecording() {
        mRecorder = new MediaRecorder();
        mRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        mRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        mRecorder.setOutputFile(mfilename);
        mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

        try {
            mRecorder.prepare();
        } catch (IOException e) {
            Log.e(LOG_TAG, "prepare() failed");
        }

        mRecorder.start();
    }

    private void stopRecording() {
        mRecorder.stop();
        mRecorder.release();
        mRecorder = null;
    }

    class RemindTask extends TimerTask {

        @Override
        public void run() {
            mRecorder.stop();
            mRecorder.reset();
            mRecorder.release();
            //mRecorder = null;
            //button.setEnabled(true);
            button.setClickable(true);
            recordingStopped();
            //button.setText("Record");

        }
    }




}

/*
//audioRecord.stop();
            //audioRecord.release();
            //dos.close();
            //isRecording = false;
private void startAudioRecording(File file) throws IOException
    {

        file.createNewFile();

        isRecording = true;

        // Create a DataOuputStream to write the audio data into the saved file.
        OutputStream os = new FileOutputStream(file);
        BufferedOutputStream bos = new BufferedOutputStream(os);
        DataOutputStream dos = new DataOutputStream(bos);



        // Create a new AudioRecord object to record the audio.
        int bufferSize = AudioRecord.getMinBufferSize(FREQUENCY, CHANNEL_CONFIGURATION, AUDIO_ENCODING);
        AudioRecord audioRecord = new AudioRecord(MediaRecorder.AudioSource.MIC, FREQUENCY, CHANNEL_CONFIGURATION, AUDIO_ENCODING, bufferSize);

        short[] buffer = new short[bufferSize];
        audioRecord.startRecording();


        while (isRecording) {
            int bufferReadResult = audioRecord.read(buffer, 0, bufferSize);
            for (int i = 0; i < bufferReadResult; i++)
                dos.writeShort(buffer[i]);
        }
    }
//File file = new File(mfilename);
        //startAudioRecording(file);
 */
