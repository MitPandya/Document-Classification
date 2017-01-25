package edu.ncsu.deepwalk;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class CreateEdgeList 
{

	public void createEdgeList(String ouputDir) throws IOException
	{
		File nounsFile = new File(ouputDir+"/nouns_mapping.txt");
		File filesFile = new File(ouputDir+"/files_mapping.txt");
		File edgesFile = new File(ouputDir+"/edges.txt");
		//
		int fileIds = 0;
		int indicatorsIds = 9000;
		int nounIds = 10000;
		
//		edgesFile.getParentFile().mkdirs();
		
		Map<String, Integer> nounsMap = new HashMap<String, Integer>();
		File f = new File(
				"/home/vijoy/deepwalk/exp_bitbybit/");

		String line = null;
		File[] dirs = f.listFiles();
		BufferedWriter nounswriter = null;
		BufferedWriter fileswriter = null;
		BufferedWriter edgeswriter = null;
		try
		{			
			FileWriter nounsfileWriter = new FileWriter(nounsFile);
			nounswriter = new BufferedWriter(nounsfileWriter);
			FileWriter filesFileWriter = new FileWriter(filesFile);
			fileswriter = new BufferedWriter(filesFileWriter);
			FileWriter edgesFileWriter = new FileWriter(edgesFile);
			edgeswriter = new BufferedWriter(edgesFileWriter);
			
			for (File dir : dirs) 
			{
				indicatorsIds++;
				if(dir ==null || !dir.isDirectory())
					continue;
				for(File file: dir.listFiles())
				{
					//reader			
					FileReader fileReader = new FileReader(file);
					BufferedReader reader = new BufferedReader(fileReader);
					//write the file id
					fileIds++;
					fileswriter.write(fileIds + "\t" + file.getAbsolutePath() + "\n");
					//add an edge to the indicator - for now there is only one
					edgeswriter.write(fileIds + "\t" + indicatorsIds + "\n");
					while ((line = reader.readLine()) != null) 
					{
						line = line.replaceAll("[.,;?!()<>{}*\\-'\"|:@%^&0-9]", " ");
						String[] words = line.split("\\s+");
						for (String str : words) 
						{
							if(!nounsMap.containsKey(str))
							{
								nounIds++;
								nounsMap.put(str, nounIds);
								//write the noun								
								nounswriter.write(nounIds + "\t" + str + "\n");
							}
							edgeswriter.write(fileIds + "\t" + nounsMap.get(str) + "\n");
						}
					}
				}
			}
		}
		finally
		{
			if(nounswriter != null && fileswriter != null && edgeswriter != null)
			{
				nounswriter.close();
				fileswriter.close();
				edgeswriter.close();
			}
		}
	}
	
	/**
	 * This reads the embeddings file and filters out ony the documents.
	 * @throws IOException
	 */
	public void getOnlyDocs() throws IOException
	{
		//reader
		File file = new File("/home/vijoy/deepwalk/edges.embeddings");
		FileReader fileReader = new FileReader(file);
		BufferedReader reader = new BufferedReader(fileReader);
		
		FileWriter filewriter = new FileWriter(new File("/home/vijoy/deepwalk/onlydoc.embeddings"));
		BufferedWriter writer = new BufferedWriter(filewriter);
		try
		{
			String line = null;
			while ((line = reader.readLine()) != null) 
			{
				String[] fields = line.split(" ");
				if(fields.length == 3 && Integer.parseInt(fields[0]) <= 9000)
				{
					writer.write(line + "\n");
				}
			}
		}
		finally
		{
			writer.close();
			reader.close();
		}
	}
	
	public static void main(String[] args) throws IOException
	{
		CreateEdgeList edgeList = new CreateEdgeList();
//		edgeList.createEdgeList("/home/vijoy/deepwalk");
		edgeList.getOnlyDocs();
	}
}
