import com.itextpdf.text.DocumentException;
import com.itextpdf.text.pdf.*;

import java.io.*;
import java.util.Arrays;
import java.util.HashMap;

/**
 * Created by Leonardo Pistone on 5/12/16.
 */
public class EmptySigner {

  public static void main(String[] args) throws IOException, DocumentException {

    System.err.println("This is EmptySigner, an itext wrapper, part of AIS.py.");

    for (String filename : args) {
      PdfReader reader = new PdfReader(filename);
      ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();

      PdfSignature pdfSignature = new PdfSignature(
          PdfName.ADOBE_PPKLITE,
          PdfName.ADBE_PKCS7_DETACHED
          );

      PdfStamper pdfStamper = PdfStamper.createSignature(reader, byteArrayOutputStream, '\0');
      PdfSignatureAppearance pdfSignatureAppearance = pdfStamper
        .getSignatureAppearance();
      pdfSignature.setReason(null);
      pdfSignature.setLocation(null);
      pdfSignature.setContact(null);
      pdfSignature.setDate(new PdfDate());
      pdfSignatureAppearance.setCryptoDictionary(pdfSignature);

      HashMap<PdfName, Integer> exc = new HashMap<PdfName, Integer>();
      exc.put(PdfName.CONTENTS, 44002);
      pdfSignatureAppearance.preClose(exc);

      PdfLiteral pdfLiteral = (PdfLiteral) pdfSignature.get(PdfName.CONTENTS);

      byte[] outc = new byte[(pdfLiteral.getPosLength() - 2) / 2];
      Arrays.fill(outc, (byte) 0);

      PdfDictionary dic2 = new PdfDictionary();
      dic2.put(PdfName.CONTENTS, new PdfString(outc).setHexWriting(true));
      pdfSignatureAppearance.close(dic2);

      OutputStream outputStream = new FileOutputStream(filename);

      byteArrayOutputStream.writeTo(outputStream);

      byteArrayOutputStream.close();
      outputStream.close();
    }
  }
}
