import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

class ChartBuilder(object):
    def __init__(self):
        mpl.style.use('ggplot')
        mpl.font_manager._rebuild()
        mpl.rcParams['font.sans-serif'] = 'FrescoPlus-Bold'
        mpl.rcParams['font.family'] = 'sans-serif'
        self.color_dark_grey = '#29323C'
        self.color_light_grey = '#EEF2F5'
        self.color_completed = '#27A8E0'
        self.color_of_lost = '#626E7A'
        self.title_font_size = 15
        self.axis_font_size = 11
        self.bar_note_font_size = 11

    def for_comparison(self, comparison):
        df = comparison.copy()
        df['Total deals'] = df['Closed deals'] + df['Lost deals']
        df['Efficency'] = df['Closed deals'] / (df['Closed deals'] + df['Lost deals']) * 100
        self.df = df
        return self

    def ordered_by_efficency(self):
        self.df = self.df.sort_values(by=['Efficency'], ascending=True).reset_index()
        return self
    
    def ordered_by_total(self):
        self.df = self.df.sort_values(by=['Total deals'], ascending=True).reset_index()
        return self

    def with_title(self, title):
        self.title = title
        return self

    def make_barchart_of(self, column_name):
        axes = self.df.plot(
            x=column_name,
            y=['Closed deals', 'Lost deals'],
            kind='barh', stacked=True,
            figsize=(25, 20),
            fontsize=self.axis_font_size,
            color=[self.color_completed, self.color_of_lost],
            legend=False,)
        axes.set_title(self.title, color=self.color_dark_grey, fontsize=self.title_font_size, pad=25)
        axes.patch.set_color(self.color_light_grey)
        axes.tick_params(colors=self.color_dark_grey)
        
        axes.set_xlabel("Number of deals", fontsize=self.axis_font_size, color=self.color_dark_grey, labelpad=10)
        axes.set_ylabel(None)
        axes.xaxis.grid(True)
        axes.yaxis.grid(False)

        self.graph = axes
        return self
        
    def with_tuned_bar_text(self, max_number_of_deals, x_margin=0, y_margin=0, disply_long_closed_deals_text_after=23):
        plt.subplots_adjust(left=0.155, right=0.98, top=0.92, bottom=0.05, wspace=0, hspace=0)
        ticks = list(i for i in range(25, max_number_of_deals + 25, 25))
        self.graph.set_xticks(ticks)
        height = 1
        
        df = self.df
        for idx, row in df.iterrows():
            total = df.at[idx, 'Total deals']
            efficency = df.at[idx, 'Efficency']
            lost_deals = df.at[idx, 'Lost deals']
            closed_deals = df.at[idx, 'Closed deals']
            y = idx * height - 0.08
            total_deals_text = ChartBuilder.make_row_summary(total, efficency)
            closed_deals_text = ChartBuilder.make_closed_deals(closed_deals, disply_long_closed_deals_text_after)
            self.graph.text(total + 1, y + y_margin, total_deals_text, fontsize=self.bar_note_font_size, color=self.color_dark_grey)
            self.graph.text(closed_deals + 1, y + y_margin, str(lost_deals), fontsize=self.bar_note_font_size, color=self.color_dark_grey)
            self.graph.text(x_margin, y + y_margin, closed_deals_text, fontsize=self.bar_note_font_size, color=self.color_dark_grey)
        return self

    @staticmethod
    def make_row_summary(total, efficency):
        if (total > 19):
            return str(total)+" deals ("+str(round(efficency, 1))+"% closed)"
        return str(total)+" deals"

    @staticmethod
    def make_closed_deals(closed_deals, closed_deals_threshold=23):
        if (closed_deals < closed_deals_threshold):
            return str(closed_deals)
        return str(closed_deals) + " deals closed"

    def build(self):
        plt.gcf().subplots_adjust(bottom=0.075)
        plt.show()

    def save(self, file_path):
        fig = plt.gcf()
        fig.set_size_inches((14.09, 9.68), forward=False)
        fig.savefig(file_path, dpi=500, orientation='landscape')


def plot_industries(industry_comparison, number_of_companies_with_industries = 639):
    column_name = 'Aggregated Industry'
    title = "Deals per Industry (based on "+str(number_of_companies_with_industries)+" / 802 companies)"
    ChartBuilder()\
        .for_comparison(industry_comparison)\
        .ordered_by_efficency()\
        .with_title(title)\
        .make_barchart_of(column_name)\
        .with_tuned_bar_text(250, 1)\
        .build()
        #.save("Deals per Industry.png")
    
def plot_sizes(size_comparison, number_of_companies_with_size=584):
    column_name = 'LinkedIn size'
    size_comparison = size_comparison.sort_index().reset_index(drop=True)
    df = size_comparison
    size_comparison = pd.concat([df.iloc[0:3], df.iloc[5:], df.iloc[[4]]]).reset_index()
    title = "Deals per "+column_name+" (based on "+str(number_of_companies_with_size)+" / 802 companies)"
    ChartBuilder()\
        .for_comparison(size_comparison)\
        .with_title(title)\
        .make_barchart_of(column_name)\
        .with_tuned_bar_text(300, x_margin=1, y_margin=0.04)\
        .build()
        #.save("Deals per LinkedIn size.png")

def plot_sources(size_comparison, number_of_deals_with_sources=400):
    column_name = 'Source'
    size_comparison = size_comparison.sort_index().reset_index(drop=True)
    df = size_comparison
    size_comparison = pd.concat([df.iloc[0:3], df.iloc[5:], df.iloc[[4]]]).reset_index()
    title = "Deals per "+column_name+" (based on "+str(number_of_deals_with_sources)+" / 1421 deals)"
    ChartBuilder()\
        .for_comparison(size_comparison)\
        .ordered_by_total()\
        .with_title(title)\
        .make_barchart_of(column_name)\
        .with_tuned_bar_text(150, x_margin=0.25, y_margin=0.04, disply_long_closed_deals_text_after=10)\
        .build()
        #.save("Deals per Source.png")

if __name__ == "__main__":
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    
    # industry_comparison = pd.read_csv(data_folder+'/tmp-industry-comparison.csv', index_col=0)
    # plot_industries(industry_comparison)

    # size_comparison = pd.read_csv(data_folder+'/tmp-linkedin-size-comparison.csv', index_col=0)
    # plot_sizes(size_comparison)

    source_comparison = pd.read_csv(data_folder+'/tmp-source-comparison.csv', index_col=0)
    plot_sources(source_comparison)