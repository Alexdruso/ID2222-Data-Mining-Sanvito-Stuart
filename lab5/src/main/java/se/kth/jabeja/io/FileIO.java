/*
 * Copyright (c) 2008
 *  
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */

package se.kth.jabeja.io;

import java.io.*;

/**
 * Class to work with text files.
 */

public class FileIO {

//----------------------------------------------------------------------------------

    /**
     * Writes a string into a file.
     *
     * @param str      Specifies the string that will be written in the file.
     * @param fileName Specifies the name.
     * @throws IOException Thrown if it can not open the file or write in it.
     */
    public static void write(String str, String fileName) throws IOException {
        Writer output = null;
        FileWriter file = new FileWriter(fileName, false);
        output = new BufferedWriter(file);
        output.write(str);
        output.close();
    }

//----------------------------------------------------------------------------------

    /**
     * Appends a string at the end of an existing file. If the file does not exist then it is created.
     *
     * @param str      Specifies the string that will be written in the file.
     * @param fileName Specifies the name of storing file.
     * @throws IOException Thrown if it can not open  the file.
     */
    public static void append(String str, String fileName) throws IOException {
        Writer output = null;
        FileWriter file = new FileWriter(fileName, true);
        output = new BufferedWriter(file);
        output.write(str);
        output.close();
    }

//----------------------------------------------------------------------------------

    /**
     * Reads the content of a file and returns it as a string.
     *
     * @param fileName Specifies the file name.
     * @return A string that contains the whole content of the file.
     * @throws IOException Thrown if the the file does not exist.
     */
    public static String read(String fileName) throws IOException {
        int numRead = 0;
        int curRead = 0;
        String str = null;

        File file = new File(fileName);
        InputStream in = new FileInputStream(file);
        long length = file.length();
        byte[] bytes = new byte[(int) length];

        while (curRead != length) {
            numRead = in.read(bytes, curRead, bytes.length - curRead);
            curRead += numRead;
        }

        str = new String(bytes);
        in.close();
        return str;
    }

}