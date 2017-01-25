import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;

public class TagAndExtract 
{

	public static void main(String[] args) throws IOException,
			ClassNotFoundException 
	{
		MaxentTagger tagger = new MaxentTagger("taggers/english-left3words-distsim.tagger");

		File f = new File("/home/vijoy/dmoz/content_by_topic/bitbybit/");

		String line = null;
		File[] dirs = f.listFiles();
		for (File dir : dirs) 
		{
			if(dir ==null || !dir.isDirectory())
				continue;
			for(File file: dir.listFiles())
			{
				FileReader fileReader = new FileReader(file);
				BufferedReader reader = new BufferedReader(fileReader);
				File output = new File("/home/vijoy/dmoz/content_by_topic/exp_bitbybit/" + dir.getName() + "/NN_" + file.getName());
				output.getParentFile().mkdirs();
				FileWriter fileWriter = new FileWriter(output);
				BufferedWriter writer = new BufferedWriter(fileWriter);
	
				while ((line = reader.readLine()) != null) 
				{
					line = line.replaceAll("[.,;?!()<>{}*\\-'\"|:@%^&0-9]", " ");
					String[] words = line.split("\\s+");
					int i =0;
					for (String str : words) 
					{
						if(i > 1000)
							break;
						List<HasWord> sentence = Sentence.toWordList(str);
						List<TaggedWord> taggedsent = tagger.tagSentence(sentence);
						for (TaggedWord tw : taggedsent) 
						{
							if (tw.tag().startsWith("NN")) 
							{
//								if (tw.tag().startsWith("VB")) {
								writer.write(tw.word() + " ");
							}
//							else
//							{
//								writer.write(tw.word() + " ");
//							}
							i++;
						}
					}
				}
				reader.close();
				writer.close();
			}
		}

	}

}