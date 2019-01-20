# coding=utf-8
import trendyolTest
import config

# ***** Run For Tests *****

# Take the instance

slave = trendyolTest.TrendyolTest()

# Choose the webdriver
# Options -> 'chrome' - 'firefox'

slave.runWebDriver('chrome')

# Go Url
slave.goUrl(config.baseUrl)

# Gender popup close
slave.closePopUp()

# Login case
slave.loginCase()

# Check the tabs and image loads
slave.checkAllTabs()

# Check the random boutique image loads
slave.checkRandomBoutiqueImages()

# Add product in basket
slave.addProductInBasket()

# Finised all tests and quit webdriver
slave.finishCase()
