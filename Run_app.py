import streamlit as st
import pandas as pd
import io
from io import BytesIO

# Define lookup tables 
SITE_LOOKUP = {
    10: 'ADCO',
    17: 'GPCO',
    18: 'GPCO',
    15: 'LSCO',
    2: 'DECO',
    4: 'CHCO',
    9: 'BFCO',
    14:'MPCO',
    8:'PVCO'
}

PROGRAM_LOOKUP = {
    'ADCO':'COATTs',
    'GPCO':'COATTs',
    'LSCO':'COATTs',
    'DECO':'COOPs',
    'CHCO':'COOPs',
    'BFCO':'COOPs',
    'MPCO':'COOPs',
    'PVCO':'COOPs'
}

PARAMETER_LOOKUP = {
    43201:'Methane',
    17141:'Naphthalene',
    17147:'Acenaphthene',
    17148:'Acenaphthylene',
    17149:'Fluorene',
    17150:'Phenanthrene',
    17151:'Anthracene',
    17201:'Fluoranthene',
    17204:'Pyrene',
    17208:'Chrysene',
    17211:'Coronene',
    17212:'Perylene',
    17215:'Benzo[a]anthracene',
    17220:'Benzo[b]fluoranthene',
    17223:'Benzo[k]fluoranthene',
    17224:'Benzo[e]pyrene',
    17231:'Dibenzo[a,h]anthracene',
    17237:'Benzo[g,h,i]perylene',
    17242:'Benzo[a]pyrene',
    17243:'Indeno[1,2,3-cd]pyrene',
    42153:'Carbon disulfide',
    43208:'1,2-Dichlorotetrafluoroethane',
    43218:'1,3-Butadiene',
    43233:'n-Octane',
    43372:'Methyl tert-butyl ether',
    43373:'Tert-amyl methyl ether',
    43396:'tert-Butyl ethyl ether',
    43438:'Ethyl acrylate',
    43441:'Methyl methacrylate',
    43502:'Formaldehyde',
    43503:'Acetaldehyde',
    43504:'Propionaldehyde',
    43509:'Acrolein',
    43510:'Butyraldehyde',
    43517:'Hexanaldehyde',
    43518:'Valeraldehyde',
    43528:'Crotonaldehyde',
    43551:'Acetone',
    43552:'Methyl ethyl ketone',
    43560:'Methyl isobutyl ketone',
    43601:'Ethylene oxide',
    43702:'Acetonitrile',
    43704:'Acrylonitrile',
    43801:'Chloromethane',
    43802:'Dichloromethane',
    43803:'Chloroform',
    43804:'Carbon tetrachloride',
    43806:'Bromoform',
    43811:'Trichlorofluoromethane',
    43812:'Chloroethane',
    43813:'1,1-Dichloroethane',
    43814:'Methyl chloroform',
    43815:'Ethylene dichloride',
    43817:'Tetrachloroethylene',
    43818:'1,1,2,2-Tetrachloroethane',
    43819:'Bromomethane',
    43820:'1,1,2-Trichloroethane',
    43821:'1,1,2-Trichloro-1,2,2-trifluoroethane',
    43823:'Dichlorodifluoromethane',
    43824:'Trichloroethylene',
    43826:'1,1-Dichloroethylene',
    43828:'Bromodichloromethane',
    43829:'1,2-Dichloropropane',
    43830:'trans-1,3-Dichloropropene',
    43831:'cis-1,3-Dichloropropene',
    43832:'Dibromochloromethane',
    43835:'Chloroprene',
    43836:'Bromochloromethane',
    43838:'trans-1,2-Dichloroethylene',
    43839:'cis-1,2-Dichloroethene',
    43843:'Ethylene dibromide',
    43844:'Hexachlorobutadiene',
    43860:'Vinyl chloride',
    45109:'m/p Xylene',
    45201:'Benzene',
    45202:'Toluene',
    45203:'Ethylbenzene',
    45204:'o-Xylene',
    45207:'1,3,5-Trimethylbenzene',
    45208:'1,2,4-Trimethylbenzene',
    45220:'Styrene',
    45501:'Benzaldehyde',
    45801:'Chlorobenzene',
    45805:'1,2-Dichlorobenzene',
    45806:'1,3-Dichlorobenzene',
    45807:'1,4-Dichlorobenzene',
    45810:'1,2,4-Trichlorobenzene',
    85102:'Antimony',
    85103:'Arsenic',
    85105:'Beryllium',
    85110:'Cadmium', 
    85112:'Chromium',
    85113:'Cobalt',
    85128:'Lead',
    85132:'Manganese',
    85136:'Nickel',
    85154:'Selenium',
    43102:'Total NMOC (non-methane organic compound)',
    43141:'n-Dodecane',
    43142:'Tridecene',
    43143:'n-Tridecane',
    43144:'Propyne',
    43145:'1-Octene',
    43202:'Ethane',
    43203:'Ethylene',
    43204:'Propane',
    43205:'Propylene',
    43206:'Acetylene',
    43212:'n-Butane',
    43214:'Isobutane',
    43216:'trans-2-Butene',
    43217:'cis-2-Butene',
    43220:'n-Pentane',
    43221:'Isopentane',
    43224:'1-Pentene',
    43225:'2-Methyl-1-butene',
    43226:'trans-2-Pentene',
    43227:'cis-2-Pentene',
    43228:'2-Methyl-2-butene',
    43230:'3-Methylpentane',
    43231:'n-Hexane',
    43232:'n-Heptane',
    43233:'n-Octane',
    43234:'4-Methyl-1-pentene',
    43235:'n-Nonane',
    43236:'2-Ethyl-1-butene',
    43238:'n-Decane',
    43242:'Cyclopentane',
    43243:'Isoprene',
    43244:'2,2-Dimethylbutane',
    43245:'1-Hexene',
    43246:'2-Methyl-1-pentene',
    43247:'2,4-Dimethylpentane',
    43248:'Cyclohexane',
    43249:'3-Methylhexane',
    43250:'2,2,4-Trimethylpentane',
    43252:'2,3,4-Trimethylpentane',
    43253:'3-Methylheptane',
    43256:'alpha.-Pinene',
    43257:'beta.-Pinene',
    43261:'Methylcyclohexane',
    43262:'Methylcyclopentane',
    43263:'2-Methylhexane',
    43270:'Isobutene',
    43279:'1-Nonene',
    43280:'1-Butene',
    43282:'3-Methyl-1-butene',
    43283:'Cyclopentene',
    43284:'2,3-Dimethylbutane',
    43285:'2-Methylpentane',
    43289:'trans-2-Hexene',
    43290:'cis-2-Hexene',
    43291:'2,3-Dimethylpentane',
    43292:'2-2-3-Trimethylpentane',
    43299:'1-Undecene',
    43328:'1-Heptene',
    43330:'Dodecene',
    43954:'n-Undecane',
    43960:'2-Methylheptane',
    45209:'n-Propylbenzene',
    45210:'Isopropylbenzene',
    45211:'o-Ethyltoluene',
    45212:'m-Ethyltoluene',
    45213:'p-Ethyltoluene',
    45218:'m-Diethylbenzene',
    45219:'p-Diethylbenzene',
    45225:'1,2,3-Trimethylbenzene'    
}

TestType_LOOKUP = {
    43201:'VOC',
    17141:'PAH',
    17147:'PAH',
    17148:'PAH',
    17149:'PAH',
    17150:'PAH',
    17151:'PAH',
    17201:'PAH',
    17204:'PAH',
    17208:'PAH',
    17211:'PAH',
    17212:'PAH',
    17215:'PAH',
    17220:'PAH',
    17223:'PAH',
    17224:'PAH',
    17231:'PAH',
    17237:'PAH',
    17242:'PAH',
    17243:'PAH',
    42153:'VOC',
    43208:'VOC',
    43218:'VOC',
    43233:'VOC',
    43372:'VOC',
    43373:'VOC',
    43396:'VOC',
    43438:'VOC',
    43441:'VOC',
    43502:'Carbonyl',
    43503:'Carbonyl',
    43504:'Carbonyl',
    43509:'VOC',
    43510:'Carbonyl',
    43517:'Carbonyl',
    43518:'Carbonyl',
    43528:'Carbonyl',
    43551:'Carbonyl',
    43552:'Carbonyl',
    43560:'VOC',
    43601:'VOC',
    43702:'VOC',
    43704:'VOC',
    43801:'VOC',
    43802:'VOC',
    43803:'VOC',
    43804:'VOC',
    43806:'VOC',
    43811:'VOC',
    43812:'VOC',
    43813:'VOC',
    43814:'VOC',
    43815:'VOC',
    43817:'VOC',
    43818:'VOC',
    43819:'VOC',
    43820:'VOC',
    43821:'VOC',
    43823:'VOC',
    43824:'VOC',
    43826:'VOC',
    43828:'VOC',
    43829:'VOC',
    43830:'VOC',
    43831:'VOC',
    43832:'VOC',
    43835:'VOC',
    43836:'VOC',
    43838:'VOC',
    43839:'VOC',
    43843:'VOC',
    43844:'VOC',
    43860:'VOC',
    45109:'VOC',
    45201:'VOC',
    45202:'VOC',
    45203:'VOC',
    45204:'VOC',
    45207:'VOC',
    45208:'VOC',
    45220:'VOC',
    45501:'Carbonyl',
    45801:'VOC',
    45805:'VOC',
    45806:'VOC',
    45807:'VOC',
    45810:'VOC',
    85102:'Metals',
    85103:'Metals',
    85105:'Metals',
    85110:'Metals', 
    85112:'Metals',
    85113:'Metals',
    85128:'Metals',
    85132:'Metals',
    85136:'Metals',
    85154:'Metals',
    43102:'VOC',
    43141:'VOC',
    43142:'VOC',
    43143:'VOC',
    43144:'VOC',
    43145:'VOC',
    43202:'VOC',
    43203:'VOC',
    43204:'VOC',
    43205:'VOC',
    43206:'VOC',
    43212:'VOC',
    43214:'VOC',
    43216:'VOC',
    43217:'VOC',
    43220:'VOC',
    43221:'VOC',
    43224:'VOC',
    43225:'VOC',
    43226:'VOC',
    43227:'VOC',
    43228:'VOC',
    43230:'VOC',
    43231:'VOC',
    43232:'VOC',
    43233:'VOC',
    43234:'VOC',
    43235:'VOC',
    43236:'VOC',
    43238:'VOC',
    43242:'VOC',
    43243:'VOC',
    43244:'VOC',
    43245:'VOC',
    43246:'VOC',
    43247:'VOC',
    43248:'VOC',
    43249:'VOC',
    43250:'VOC',
    43252:'VOC',
    43253:'VOC',
    43256:'VOC',
    43257:'VOC',
    43261:'VOC',
    43262:'VOC',
    43263:'VOC',
    43270:'VOC',
    43279:'VOC',
    43280:'VOC',
    43282:'VOC',
    43283:'VOC',
    43284:'VOC',
    43285:'VOC',
    43289:'VOC',
    43290:'VOC',
    43291:'VOC',
    43292:'VOC',
    43299:'VOC',
    43328:'VOC',
    43330:'VOC',
    43954:'VOC',
    43960:'VOC',
    45209:'VOC',
    45210:'VOC',
    45211:'VOC',
    45212:'VOC',
    45213:'VOC',
    45218:'VOC',
    45219:'VOC',
    45225:'VOC'    
}

st.title("AQS Text File Processor")
st.write("Upload a pipe-delimited text file to process and download the modified version")

# Show lookup table
with st.expander("View Lookup Tables"):
    st.dataframe(pd.DataFrame(list(SITE_LOOKUP.items()), columns=["Code", "Site"]))
    st.dataframe(pd.DataFrame(list(PROGRAM_LOOKUP.items()), columns=["Site", "Program"]))
    st.dataframe(pd.DataFrame(list(PARAMETER_LOOKUP.items()), columns=["Parameter Code", "Analyte"]))
    st.dataframe(pd.DataFrame(list(TestType_LOOKUP.items()), columns=["Parameter Code", "Test Type"]))


uploaded_file = st.file_uploader("Choose a text file", type="txt")

if uploaded_file is not None:
    # Read and display original content
    content = uploaded_file.getvalue().decode("utf-8")
    st.subheader("Original File Content")
    st.text_area("Original text", content, height=200)
    
    try:
        # Simple processing approach - split by lines
        lines = content.strip().split('\n')
        
        if len(lines) >= 2:
            # Save the header row
            st.info(f"Using first row as headers")
            
            # Remove the second row
            st.info(f"Removing second row")
            lines.pop(1)
            
            # Rejoin and parse as DataFrame
            modified_content = '\n'.join(lines)
            df = pd.read_csv(io.StringIO(modified_content), delimiter='|', encoding='utf-8')
            
            # Display DataFrame after row removal
            st.subheader("DataFrame after removing second row")
            st.dataframe(df.head())
            
            # Add the new columns
            #convert the site codes to our acronyms: 
            df['Site'] = df['Site ID'].map(SITE_LOOKUP)
            df['Analyte'] = df['Parameter'].map(PARAMETER_LOOKUP)  
            df['Test_Type'] = df['Parameter'].map(TestType_LOOKUP)
            df['Program'] = df['Site'].map(PROGRAM_LOOKUP)  
                        
            # Display final DataFrame
            st.subheader("Final DataFrame with added columns")
            st.dataframe(df.head())
            
            # Successful mappings
            mapped_sites = len(df[df['Site'] != "Unknown"])
            mapped_analytes = len(df[df['Analyte'] != "Unknown"])
            mapped_testtypes = len(df[df['Test_Type'] != "Unknown"])
            mapped_programs = len(df[df['Program'] != "Unknown"])
            
            st.write(f"Successfully mapped {mapped_sites} out of {len(df)} site IDs ({mapped_sites/len(df)*100:.1f}%)")
            st.write(f"Successfully mapped {mapped_analytes} out of {len(df)} parameter ({mapped_analytes/len(df)*100:.1f}%)")
            st.write(f"Successfully mapped {mapped_testtypes} out of {len(df)} test types ({mapped_testtypes/len(df)*100:.1f}%)")
            st.write(f"Successfully mapped {mapped_programs} out of {len(df)} programs ({mapped_programs/len(df)*100:.1f}%)")

            # Create an Excel file in memory
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)

                
            excel_data = buffer.getvalue()

            # Download button for Excel file
            st.download_button(
                label="Download Excel file",
                data=excel_data,
                file_name="processed_file.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            
            st.success("Ta-Da, processing complete! File ready for download.")
        else:
            st.warning("File doesn't have enough rows to remove the second row")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        # Check if 'Site ID' column is missing 
        if "Site ID" in str(e):
            st.warning("The column 'Site ID' was not found in your file. Please verify your file format.")
        if "Parameter" in str(e):
            st.warning("The column 'Parameter' was not found in your file. Please verify your file format.")