from transformers import AutoTokenizer, AutoModelForCausalLM,LlamaTokenizer
import transformers
import torch
from peft import AutoPeftModelForCausalLM, PeftModel
import pandas as pd 



def mergj_models () :
    tokenizer = AutoTokenizer.from_pretrained('sharpbai/Llama-2-7b-hf')
    base_model_name = "sharpbai/Llama-2-7b-hf" # change for your basemodel


    new_model_name = "/content/sizifs-llma-v1.3"
    model_path = "/content/sizifs-llma-v1.4"


    #device_map = {"": 0} # single gpu?

    base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float16,
    #device_map=device_map,
    offload_folder="offload",
    offload_state_dict = True
    )
    model = PeftModel.from_pretrained(
        base_model,
        new_model_name,
        use_ram_optimized_load=False,
        offload_folder="offload")
    merged_model = model.merge_and_unload()


    merged_model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)


def GetResponse(us_input):

    
    
    path_to_model = "/Users/avilya/Downloads/train_dataset_dataset/sizifs-llma-v1.4"
    #device_map = {"": 0} # single gpu?

    model = AutoModelForCausalLM.from_pretrained(path_to_model,
    low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float32,
    #device_map=device_map,
    offload_folder = path_to_model,
    offload_state_dict = False)

    tokenizer = AutoTokenizer.from_pretrained(path_to_model)
    

    promt = "User: {}\nAI:".format(us_input)
    input_ids = tokenizer.encode(promt, return_tensors="pt")
    #output = model.generate(input_ids, max_length=512, num_return_sequences=1)

    #print(tokenizer.decode(output[0], skip_special_tokens=True))

def checkQestion(user_input) : 
    df = pd.read_excel("output.xlsx")
    all_ans = []
    all_quest = []
    for i in range(len(df['answers_merged'])):
        a = eval(df['answers_merged'][i])
        b = eval(df['questions_merged'][i])
        all_ans.append(a)
        all_quest.append(b)
    for i in range(len(all_quest)) : 
        if user_input in all_quest[i]:
            return all_ans[i]



print(checkQestion("Зачем нужны ПТЭ?"))