# -*- coding: UTF-8 -*-
import scrapy

from jinja2 import Environment, FileSystemLoader, select_autoescape
from os import path
from urllib.parse import urljoin
from git import Repo


class NotesSpider(scrapy.Spider):
    name = 'Notes'
    start_urls = [
        'https://baiyangcao.github.io/'
        # 'http://localhost:4000/'
    ]
    repo_path = r'E:\Notes'
    readme_path = None
    index_path = None
    data = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html', 'md'])
        )

    def parse(self, response):
        for post in response.css('#main-content h1'):
            json = {
                'text': post.css('a::text').extract_first(),
                'url': urljoin(self.start_urls[0], post.css('a::attr("href")').extract_first())
            }
            # yield json
            self.data.append(json)

        next_url = response.css('li.next a::attr("href")').extract_first()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def close(self, reason):
        self.generate_readme()
        self.generate_index()
        self.push_repo()

    def generate_readme(self):
        '''
        generate readme.md
        :return: 
        '''
        try:
            readme_tempalte = self.env.get_template('README.md')
            readme = readme_tempalte.render(notes=self.data).encode('utf-8')
            self.readme_path = getattr(self, 'readme', 'README.md')
            with open(self.readme_path, 'wb') as file:
                file.write(readme)
                print('generate README.md successfully')
        except Exception as ex:
            print('generate README.md error: ', ex)

    def generate_index(self):
        '''
        generate docs/index.html 
        :return: 
        '''
        try:
            index_template = self.env.get_template('index.html')
            index = index_template.render(notes=self.data).encode('utf-8')
            index_name = getattr(self, 'index', 'index.html')
            self.index_path = path.join('docs', index_name)
            with open(self.index_path, 'wb') as file:
                file.write(index)
                print('generate index.html successfully')
        except Exception as ex:
            print('generate index.html error: ', ex)

    def push_repo(self):
        '''
        add readme.md, index.html file to stage, commit, push to remote
        :return: 
        '''
        repo = Repo(self.repo_path)
        index = repo.index

        # commit
        index.add([self.readme_path, self.index_path])
        index.commit('update readme.md and index.html automatically')

        # push
        remote = repo.remote('github')
        remote.push()
