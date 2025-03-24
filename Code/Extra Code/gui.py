from Main import getUrl



# Function to call getUrl and handle URL and file name inputs
def f1(href_link):
    # update_label_color("grey")  # Set label to grey initially to indicate processing

    print("\n\n href_link:- ",href_link)

    name = href_link
    company_data = name.split("/")[-2].capitalize()

    n = 9
    # Check if "moneycontrol" exists in the URL
    if "moneycontrol" in name:
        dir_list = [str(i) for i in range(n, 0, -1)]
        print(dir_list)
        
        for i in range(0, n):
            print("\nLoop start")
            if i == 0:
                link = href_link
                print(f"{i} -> {link}")
                file = dir_list[i]
            else:
                url = href_link.split("/")
                string = url[-1]
                print("\n\n String:- ", string)

                # Find the position of #
                j = string.find('#')
                print("\n\n j:- ", j)
                
                if j != -1:
                    modified_string = string[:j] + f"/{i+1}" + string[j:]
                    print("\n modified_string", modified_string)


                print("\n\n Split modified String:- ", modified_string.split("/"))
                url[-1] = modified_string
                link = '/'.join(url)
                print(f"\n\n{i} -> {link}")
                file = dir_list[i]
            
            # Call getUrl function and check result
            result = getUrl(link, file, "moneycontrol", company_data[:-2])
            
        return "Sucess" if result else "Failure"

if __name__ == "__main__":
    link = "https://www.moneycontrol.com/financials/ltimindtree/results/quarterly-results/LI12/7#LI12"
    
    message = f1(link)
    
    print(message)